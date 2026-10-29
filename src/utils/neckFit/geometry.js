/**
 * Geometry utilities for neck-fit collar modeling.
 */

/** @typedef {{ x: number, y: number }} Point */

/**
 * @param {Point[]} points
 * @returns {number}
 */
export function polygonPerimeter(points) {
  if (!points || points.length < 2) return 0;
  let p = 0;
  for (let i = 0; i < points.length; i++) {
    const a = points[i];
    const b = points[(i + 1) % points.length];
    p += Math.hypot(b.x - a.x, b.y - a.y);
  }
  return p;
}

/**
 * @param {Point[]} points
 * @returns {Point}
 */
export function polygonCentroid(points) {
  let cx = 0;
  let cy = 0;
  for (const p of points) {
    cx += p.x;
    cy += p.y;
  }
  const n = points.length || 1;
  return { x: cx / n, y: cy / n };
}

/**
 * Scale a closed profile uniformly so its perimeter matches targetPerimeter.
 * @param {Point[]} points
 * @param {number} targetPerimeter
 * @returns {Point[]}
 */
export function scaleProfileToPerimeter(points, targetPerimeter) {
  const current = polygonPerimeter(points);
  if (current <= 0 || targetPerimeter <= 0) return points.map((p) => ({ ...p }));
  const scale = targetPerimeter / current;
  const c = polygonCentroid(points);
  return points.map((p) => ({
    x: c.x + (p.x - c.x) * scale,
    y: c.y + (p.y - c.y) * scale,
  }));
}

/**
 * Smooth a closed polygon with weighted moving average.
 * @param {Point[]} points
 * @param {number} level 0-1 smoothing strength
 * @returns {Point[]}
 */
export function smoothPolygon(points, level) {
  if (level <= 0 || points.length < 4) return points.map((p) => ({ ...p }));
  const passes = Math.max(1, Math.round(level * 4));
  let result = points.map((p) => ({ ...p }));
  for (let pass = 0; pass < passes; pass++) {
    const next = [];
    const n = result.length;
    for (let i = 0; i < n; i++) {
      const prev = result[(i - 1 + n) % n];
      const curr = result[i];
      const nextPt = result[(i + 1) % n];
      next.push({
        x: prev.x * 0.25 + curr.x * 0.5 + nextPt.x * 0.25,
        y: prev.y * 0.25 + curr.y * 0.5 + nextPt.y * 0.25,
      });
    }
    result = next;
  }
  return result;
}

/**
 * Offset a closed polygon outward by distance (positive = outward).
 * @param {Point[]} points
 * @param {number} distance
 * @returns {Point[]}
 */
export function offsetPolygon(points, distance) {
  if (distance === 0) return points.map((p) => ({ ...p }));
  const n = points.length;
  const result = [];
  for (let i = 0; i < n; i++) {
    const prev = points[(i - 1 + n) % n];
    const curr = points[i];
    const next = points[(i + 1) % n];

    const e1x = curr.x - prev.x;
    const e1y = curr.y - prev.y;
    const e2x = next.x - curr.x;
    const e2y = next.y - curr.y;

    const len1 = Math.hypot(e1x, e1y) || 1;
    const len2 = Math.hypot(e2x, e2y) || 1;

    // Outward normals (assuming CCW winding)
    const n1x = e1y / len1;
    const n1y = -e1x / len1;
    const n2x = e2y / len2;
    const n2y = -e2x / len2;

    let nx = n1x + n2x;
    let ny = n1y + n2y;
    const nlen = Math.hypot(nx, ny) || 1;
    nx /= nlen;
    ny /= nlen;

    result.push({
      x: curr.x + nx * distance,
      y: curr.y + ny * distance,
    });
  }
  return result;
}

/**
 * Build cumulative arc-length table for a closed polyline.
 * @param {Point[]} points
 * @returns {{ points: Point[], cumulative: number[], total: number }}
 */
export function buildArcLengthTable(points) {
  const n = points.length;
  const cumulative = [0];
  for (let i = 0; i < n; i++) {
    const a = points[i];
    const b = points[(i + 1) % n];
    cumulative.push(cumulative[cumulative.length - 1] + Math.hypot(b.x - a.x, b.y - a.y));
  }
  return { points, cumulative, total: cumulative[cumulative.length - 1] };
}

/**
 * @param {{ points: Point[], cumulative: number[], total: number }} table
 * @param {number} s arc length (wrapped)
 * @returns {Point}
 */
export function getPointAtS(table, s) {
  const { points, cumulative, total } = table;
  if (total <= 0) return { x: 0, y: 0 };
  let dist = ((s % total) + total) % total;
  for (let i = 0; i < points.length; i++) {
    const segStart = cumulative[i];
    const segEnd = cumulative[i + 1];
    if (dist >= segStart && dist <= segEnd) {
      const t = segEnd === segStart ? 0 : (dist - segStart) / (segEnd - segStart);
      const a = points[i];
      const b = points[(i + 1) % points.length];
      return {
        x: a.x + t * (b.x - a.x),
        y: a.y + t * (b.y - a.y),
      };
    }
  }
  return { ...points[0] };
}

/**
 * @param {{ points: Point[], cumulative: number[], total: number }} table
 * @param {number} s
 * @returns {Point} unit tangent
 */
export function getTangentAtS(table, s) {
  const delta = 0.5;
  const p1 = getPointAtS(table, s - delta);
  const p2 = getPointAtS(table, s + delta);
  const len = Math.hypot(p2.x - p1.x, p2.y - p1.y) || 1;
  return { x: (p2.x - p1.x) / len, y: (p2.y - p1.y) / len };
}

/**
 * Extract path segment from s0 to s1 (may wrap).
 * @param {{ points: Point[], cumulative: number[], total: number }} table
 * @param {number} s0
 * @param {number} s1
 * @param {number} [samples=40]
 * @returns {Point[]}
 */
export function extractPathSegment(table, s0, s1, samples = 40) {
  const { total } = table;
  if (total <= 0) return [];
  let length = s1 - s0;
  if (length <= 0) length += total;
  const step = length / samples;
  const pts = [];
  for (let i = 0; i <= samples; i++) {
    pts.push(getPointAtS(table, s0 + i * step));
  }
  return pts;
}

/**
 * Closest point on a closed polyline to p.
 * Uses a segment grid built once per path so repeated queries (fit search,
 * contact pads) do not rescan every edge.
 * @param {Point} p
 * @param {{ points: Point[], cumulative: number[], total: number, _spatial?: object }} table
 * @returns {{ point: Point, distance: number }}
 */
export function closestPointOnClosedPath(p, table) {
  const { points } = table;
  if (!points?.length) return { point: { x: 0, y: 0 }, distance: Infinity };
  const spatial = spatialIndexFor(points);
  let bestDist = Infinity;
  let bestIndex = Infinity;
  let bestX = points[0].x;
  let bestY = points[0].y;
  querySpatialEdges(spatial, p.x, p.y, (edge, note) => {
    const proj = projectOntoEdge(p.x, p.y, edge);
    note(proj.dist);
    // Match a full edge scan: strict <, and the lowest index wins exact ties.
    if (proj.dist < bestDist || (proj.dist === bestDist && edge.i < bestIndex)) {
      bestDist = proj.dist;
      bestIndex = edge.i;
      bestX = proj.x;
      bestY = proj.y;
    }
  });
  return { point: { x: bestX, y: bestY }, distance: bestDist };
}

/**
 * Sample points along a line segment.
 * @param {Point} a
 * @param {Point} b
 * @param {number} count
 * @returns {Point[]}
 */
export function sampleLine(a, b, count) {
  const pts = [];
  for (let i = 0; i <= count; i++) {
    pts.push(lerpPoint(a, b, i / count));
  }
  return pts;
}

/** Radii above this are treated as straight rigid segments. */
export const RIGID_STRAIGHT_BEND_RADIUS = 2500;

/**
 * Rigid circular-arc centerline with fixed arc length (inextensible, fixed curvature).
 * @param {Point} start
 * @param {Point} startTangent unit vector at start
 * @param {number} arcLength mm along the arc
 * @param {number} bendRadius mm — center of curvature to the left of startTangent
 * @param {number} [samples=12]
 * @returns {Point[]}
 */
export function buildRigidArcPath(start, startTangent, arcLength, bendRadius, samples = 12) {
  if (arcLength <= 0) return [start];
  if (!Number.isFinite(bendRadius) || bendRadius >= RIGID_STRAIGHT_BEND_RADIUS) {
    const end = {
      x: start.x + startTangent.x * arcLength,
      y: start.y + startTangent.y * arcLength,
    };
    return sampleLine(start, end, samples);
  }

  const R = Math.max(bendRadius, arcLength / (Math.PI * 1.95));
  const nx = -startTangent.y;
  const ny = startTangent.x;
  const center = { x: start.x + nx * R, y: start.y + ny * R };
  const startAngle = Math.atan2(start.y - center.y, start.x - center.x);
  const deltaAngle = arcLength / R;

  const pts = [];
  for (let i = 0; i <= samples; i++) {
    const angle = startAngle + deltaAngle * (i / samples);
    pts.push({
      x: center.x + R * Math.cos(angle),
      y: center.y + R * Math.sin(angle),
    });
  }
  return pts;
}

/**
 * Unit tangent at the exit of a rigid arc segment.
 * @param {Point} start
 * @param {Point} startTangent
 * @param {number} arcLength
 * @param {number} bendRadius
 * @returns {Point}
 */
export function rigidArcExitTangent(start, startTangent, arcLength, bendRadius) {
  if (
    arcLength <= 0 ||
    !Number.isFinite(bendRadius) ||
    bendRadius >= RIGID_STRAIGHT_BEND_RADIUS
  ) {
    return { ...startTangent };
  }

  const R = Math.max(bendRadius, arcLength / (Math.PI * 1.95));
  const nx = -startTangent.y;
  const ny = startTangent.x;
  const center = { x: start.x + nx * R, y: start.y + ny * R };
  const startAngle = Math.atan2(start.y - center.y, start.x - center.x);
  const endAngle = startAngle + arcLength / R;
  return { x: -Math.sin(endAngle), y: Math.cos(endAngle) };
}

/**
 * Max penetration of a polyline into a polygon.
 * @param {Point[]} points
 * @param {Point[]} polygon
 * @returns {number}
 */
export function maxPolylinePolygonPenetration(points, polygon) {
  let maxDepth = 0;
  for (let i = 0; i < points.length - 1; i++) {
    maxDepth = Math.max(
      maxDepth,
      maxLinePolygonPenetration(points[i], points[i + 1], polygon)
    );
  }
  return maxDepth;
}

/**
 * Unit tangent at the end of a polyline (direction of the last segment).
 * @param {Point[]} points
 * @param {Point} [fallback]
 * @returns {Point}
 */
export function polylineExitTangent(points, fallback = { x: 1, y: 0 }) {
  if (points.length < 2) return { ...fallback };
  const a = points[points.length - 2];
  const b = points[points.length - 1];
  const len = Math.hypot(b.x - a.x, b.y - a.y) || 1;
  return { x: (b.x - a.x) / len, y: (b.y - a.y) / len };
}

/**
 * Unit tangent at the start of a polyline (direction of the first segment).
 * @param {Point[]} points
 * @param {Point} [fallback]
 * @returns {Point}
 */
export function polylineEntryTangent(points, fallback = { x: 1, y: 0 }) {
  if (points.length < 2) return { ...fallback };
  const a = points[0];
  const b = points[1];
  const len = Math.hypot(b.x - a.x, b.y - a.y) || 1;
  return { x: (b.x - a.x) / len, y: (b.y - a.y) / len };
}

/**
 * Line segment perpendicular to a tangent, extending toward a reference point.
 * @param {Point} anchor
 * @param {Point} tangent unit vector along the parent segment
 * @param {number} length mm
 * @param {Point} towardPoint picks the inward normal side (e.g. neck centroid)
 * @returns {Point[]}
 */
export function buildPerpendicularSegment(anchor, tangent, length, towardPoint) {
  if (length <= 0) return [anchor];
  const nx = -tangent.y;
  const ny = tangent.x;
  const toRef = { x: towardPoint.x - anchor.x, y: towardPoint.y - anchor.y };
  const sign = nx * toRef.x + ny * toRef.y >= 0 ? 1 : -1;
  return [
    anchor,
    {
      x: anchor.x + sign * nx * length,
      y: anchor.y + sign * ny * length,
    },
  ];
}

/**
 * Static contact probe perpendicular to hardware, stopping at neck skin or max length.
 * Never extends into the neck interior.
 * @param {Point} anchor
 * @param {Point} tangent unit vector along parent segment
 * @param {number} maxLength mm
 * @param {Point[]} neckPoints neck skin polygon
 * @param {Point} towardPoint inward reference (e.g. neck centroid)
 * @returns {Point[]}
 */
export function buildStaticContactToNeck(anchor, tangent, maxLength, neckPoints, towardPoint) {
  if (maxLength <= 0) return [anchor];
  const end = buildPerpendicularSegment(anchor, tangent, maxLength, towardPoint)[1];
  const dx = end.x - anchor.x;
  const dy = end.y - anchor.y;
  const fullLen = Math.hypot(dx, dy);
  if (fullLen < 1e-6) return [anchor];
  const dir = { x: dx / fullLen, y: dy / fullLen };

  let tipLen = 0;
  for (let d = 0.5; d <= maxLength; d += 0.5) {
    const p = { x: anchor.x + dir.x * d, y: anchor.y + dir.y * d };
    if (pointInPolygon(p, neckPoints)) break;
    tipLen = d;
    if (pointToPolygonBoundary(p, neckPoints) <= 0.35) break;
  }

  if (tipLen <= 0) return [anchor];
  return [
    anchor,
    { x: anchor.x + dir.x * tipLen, y: anchor.y + dir.y * tipLen },
  ];
}

export function rotateVector(v, angleRad) {
  const c = Math.cos(angleRad);
  const s = Math.sin(angleRad);
  return { x: v.x * c - v.y * s, y: v.x * s + v.y * c };
}

/**
 * Angle between two unit vectors in degrees.
 * @param {Point} u
 * @param {Point} v
 * @returns {number}
 */
export function angleBetweenDeg(u, v) {
  const dot = u.x * v.x + u.y * v.y;
  const clamped = Math.max(-1, Math.min(1, dot));
  return (Math.acos(clamped) * 180) / Math.PI;
}

/**
 * Polyline length.
 * @param {Point[]} points
 * @returns {number}
 */
export function polylineLength(points) {
  let len = 0;
  for (let i = 1; i < points.length; i++) {
    len += Math.hypot(points[i].x - points[i - 1].x, points[i].y - points[i - 1].y);
  }
  return len;
}

/** Thickness multiplier for the GPS half farthest from electronics. */
export const GPS_STRAP_HALF_THICKNESS_FACTOR = 2;

/**
 * Split a polyline at a fraction of its arc length.
 * @param {Point[]} path
 * @param {number} [fraction=0.5]
 * @returns {[Point[], Point[]]} [from start, toward end] — shares one join point
 */
export function splitPolylineAtArcLength(path, fraction = 0.5) {
  if (path.length < 2) return [path, path.length ? [path[path.length - 1]] : []];
  const total = polylineLength(path);
  if (total <= 0) return [path, [path[path.length - 1]]];

  const target = total * Math.max(0, Math.min(1, fraction));
  if (target <= 0) return [[path[0]], path];
  if (target >= total) return [path, [path[path.length - 1]]];

  let acc = 0;
  for (let i = 0; i < path.length - 1; i++) {
    const a = path[i];
    const b = path[i + 1];
    const segLen = Math.hypot(b.x - a.x, b.y - a.y);
    if (acc + segLen >= target) {
      const t = segLen > 0 ? (target - acc) / segLen : 0;
      const mid = lerpPoint(a, b, t);
      return [[...path.slice(0, i + 1), mid], [mid, ...path.slice(i + 1)]];
    }
    acc += segLen;
  }
  return [path, [path[path.length - 1]]];
}

/**
 * Resample closed polyline to N evenly spaced points by arc length.
 * @param {Point[]} points
 * @param {number} count
 * @returns {Point[]}
 */
export function resampleClosedPolyline(points, count) {
  const table = buildArcLengthTable(points);
  const result = [];
  for (let i = 0; i < count; i++) {
    const s = (i / count) * table.total;
    result.push(getPointAtS(table, s));
  }
  return result;
}

/**
 * Distance from point to line segment.
 * @param {Point} p
 * @param {Point} a
 * @param {Point} b
 * @returns {number}
 */
export function pointToSegmentDistance(p, a, b) {
  const dx = b.x - a.x;
  const dy = b.y - a.y;
  const lenSq = dx * dx + dy * dy;
  if (lenSq === 0) return Math.hypot(p.x - a.x, p.y - a.y);
  let t = ((p.x - a.x) * dx + (p.y - a.y) * dy) / lenSq;
  t = Math.max(0, Math.min(1, t));
  const proj = { x: a.x + t * dx, y: a.y + t * dy };
  return Math.hypot(p.x - proj.x, p.y - proj.y);
}

/**
 * Max gap between straight segment and path segment.
 * @param {Point} lineA
 * @param {Point} lineB
 * @param {Point[]} pathPoints
 * @returns {number}
 */
export function maxGapToLine(lineA, lineB, pathPoints) {
  let maxGap = 0;
  for (const p of pathPoints) {
    maxGap = Math.max(maxGap, pointToSegmentDistance(p, lineA, lineB));
  }
  return maxGap;
}

/**
 * Check if line segment intersects polygon (simple ray crossing count).
 * @param {Point} a
 * @param {Point} b
 * @param {Point[]} polygon
 * @returns {number} max penetration depth (0 if no intersection)
 */
export function maxLinePolygonPenetration(a, b, polygon) {
  let maxDepth = 0;
  // Sample along line and check if inside polygon
  const samples = 20;
  for (let i = 0; i <= samples; i++) {
    const t = i / samples;
    const p = { x: a.x + t * (b.x - a.x), y: a.y + t * (b.y - a.y) };
    if (pointInPolygon(p, polygon)) {
      const dist = pointToPolygonBoundary(p, polygon);
      maxDepth = Math.max(maxDepth, dist);
    }
  }
  return maxDepth;
}

/**
 * @param {Point} p
 * @param {Point[]} polygon
 * @returns {boolean}
 */
export function pointInPolygon(p, polygon) {
  return pointInPolygonXY(p.x, p.y, polygon);
}

/**
 * @param {number} x
 * @param {number} y
 * @param {Point[]} polygon
 * @returns {boolean}
 */
export function pointInPolygonXY(x, y, polygon) {
  if (!polygon?.length) return false;
  const spatial = spatialIndexFor(polygon);
  if (
    x < spatial.minX ||
    x > spatial.maxX ||
    y < spatial.minY ||
    y > spatial.maxY
  ) {
    return false;
  }
  let inside = false;
  const edges = spatial.edges;
  for (let i = 0; i < edges.length; i++) {
    const e = edges[i];
    const yi = e.ay;
    const yj = e.by;
    const intersect =
      (yi > y) !== (yj > y) &&
      x < ((e.bx - e.ax) * (y - yi)) / (yj - yi + 1e-12) + e.ax;
    if (intersect) inside = !inside;
  }
  return inside;
}

/**
 * @param {Point} p
 * @param {Point[]} polygon
 * @returns {number}
 */
export function pointToPolygonBoundary(p, polygon) {
  return pointToPolygonBoundaryXY(p.x, p.y, polygon);
}

/**
 * @param {number} x
 * @param {number} y
 * @param {Point[]} polygon
 * @returns {number}
 */
export function pointToPolygonBoundaryXY(x, y, polygon) {
  if (!polygon?.length) return Infinity;
  const spatial = spatialIndexFor(polygon);
  let minDist = Infinity;
  querySpatialEdges(spatial, x, y, (edge, note) => {
    const dist = projectOntoEdge(x, y, edge).dist;
    note(dist);
    if (dist < minDist) minDist = dist;
  });
  return minDist;
}

const polygonSpatialCache = new WeakMap();

/**
 * Segment grid for a closed polygon. Cached per point-array identity.
 * Polygons must not be mutated after the first query.
 * @param {Point[]} polygon
 */
function spatialIndexFor(polygon) {
  let spatial = polygonSpatialCache.get(polygon);
  if (!spatial) {
    spatial = buildPolygonSpatialIndex(polygon);
    polygonSpatialCache.set(polygon, spatial);
  }
  return spatial;
}

/**
 * @param {Point[]} points
 */
function buildPolygonSpatialIndex(points) {
  const n = points.length;
  const edges = new Array(n);
  let minX = Infinity;
  let minY = Infinity;
  let maxX = -Infinity;
  let maxY = -Infinity;
  for (let i = 0; i < n; i++) {
    const a = points[i];
    const b = points[(i + 1) % n];
    const dx = b.x - a.x;
    const dy = b.y - a.y;
    if (a.x < minX) minX = a.x;
    if (a.y < minY) minY = a.y;
    if (a.x > maxX) maxX = a.x;
    if (a.y > maxY) maxY = a.y;
    if (b.x < minX) minX = b.x;
    if (b.y < minY) minY = b.y;
    if (b.x > maxX) maxX = b.x;
    if (b.y > maxY) maxY = b.y;
    edges[i] = {
      i,
      ax: a.x,
      ay: a.y,
      bx: b.x,
      by: b.y,
      dx,
      dy,
      lenSq: dx * dx + dy * dy,
      minX: a.x < b.x ? a.x : b.x,
      maxX: a.x < b.x ? b.x : a.x,
      minY: a.y < b.y ? a.y : b.y,
      maxY: a.y < b.y ? b.y : a.y,
    };
  }

  const cellSize = 12;
  const cols = Math.max(1, Math.ceil((maxX - minX) / cellSize) || 1);
  const rows = Math.max(1, Math.ceil((maxY - minY) / cellSize) || 1);
  const cells = new Array(cols * rows);
  for (let i = 0; i < cells.length; i++) cells[i] = [];
  for (let i = 0; i < n; i++) {
    const e = edges[i];
    const c0 = clampIndex(Math.floor((e.minX - minX) / cellSize), cols);
    const c1 = clampIndex(Math.floor((e.maxX - minX) / cellSize), cols);
    const r0 = clampIndex(Math.floor((e.minY - minY) / cellSize), rows);
    const r1 = clampIndex(Math.floor((e.maxY - minY) / cellSize), rows);
    for (let r = r0; r <= r1; r++) {
      for (let c = c0; c <= c1; c++) {
        cells[r * cols + c].push(i);
      }
    }
  }

  return {
    edges,
    cells,
    cols,
    rows,
    minX,
    minY,
    maxX,
    maxY,
    cellSize,
    stamps: new Uint32Array(n),
    stamp: 1,
  };
}

function clampIndex(index, size) {
  if (index < 0) return 0;
  if (index >= size) return size - 1;
  return index;
}

/**
 * Visit edges that can be the closest to (x, y), using expanding cell rings.
 * `note(dist)` must be called with each candidate distance so the search can stop.
 * @param {ReturnType<typeof buildPolygonSpatialIndex>} spatial
 * @param {number} x
 * @param {number} y
 * @param {(edge: object, note: (dist: number) => void) => void} visit
 */
function querySpatialEdges(spatial, x, y, visit) {
  const { edges, cells, cols, rows, minX, minY, cellSize, stamps } = spatial;
  if (!edges.length) return;

  let stamp = spatial.stamp + 1;
  if (stamp >= 0xffffffff) {
    stamps.fill(0);
    stamp = 1;
  }
  spatial.stamp = stamp;

  const col = Math.floor((x - minX) / cellSize);
  const row = Math.floor((y - minY) / cellSize);
  const maxRing =
    Math.max(cols, rows, Math.abs(col), Math.abs(row), Math.abs(col - cols), Math.abs(row - rows)) + 1;
  let best = Infinity;
  const note = (dist) => {
    if (dist < best) best = dist;
  };

  for (let ring = 0; ring <= maxRing; ring++) {
    const c0 = col - ring;
    const c1 = col + ring;
    const r0 = row - ring;
    const r1 = row + ring;
    for (let r = r0; r <= r1; r++) {
      if (r < 0 || r >= rows) continue;
      const rowOnEdge = r === r0 || r === r1;
      for (let c = c0; c <= c1; c++) {
        if (c < 0 || c >= cols) continue;
        if (ring !== 0 && !rowOnEdge && c !== c0 && c !== c1) continue;
        const bucket = cells[r * cols + c];
        for (let k = 0; k < bucket.length; k++) {
          const edgeIndex = bucket[k];
          if (stamps[edgeIndex] === stamp) continue;
          const edge = edges[edgeIndex];
          if (
            best < Infinity &&
            (x < edge.minX - best ||
              x > edge.maxX + best ||
              y < edge.minY - best ||
              y > edge.maxY + best)
          ) {
            continue;
          }
          stamps[edgeIndex] = stamp;
          visit(edge, note);
        }
      }
    }

    if (best < Infinity && ring < maxRing) {
      const left = minX + (col - ring) * cellSize;
      const right = minX + (col + ring + 1) * cellSize;
      const bottom = minY + (row - ring) * cellSize;
      const top = minY + (row + ring + 1) * cellSize;
      const exitDist = Math.min(x - left, right - x, y - bottom, top - y);
      if (exitDist >= best) break;
    }
  }
}

function projectOntoEdge(px, py, edge) {
  if (edge.lenSq === 0) {
    const dx = px - edge.ax;
    const dy = py - edge.ay;
    return { x: edge.ax, y: edge.ay, dist: Math.hypot(dx, dy) };
  }
  let t = ((px - edge.ax) * edge.dx + (py - edge.ay) * edge.dy) / edge.lenSq;
  if (t < 0) t = 0;
  else if (t > 1) t = 1;
  const x = edge.ax + t * edge.dx;
  const y = edge.ay + t * edge.dy;
  return { x, y, dist: Math.hypot(px - x, py - y) };
}

/**
 * Compute curvature along a polyline path.
 * @param {Point[]} points
 * @returns {{ curvatures: number[], maxCurvature: number, minBendRadius: number }}
 */
export function computeCurvature(points) {
  const curvatures = [];
  let maxCurvature = 0;
  for (let i = 1; i < points.length - 1; i++) {
    const p0 = points[i - 1];
    const p1 = points[i];
    const p2 = points[i + 1];
    const a = Math.hypot(p1.x - p0.x, p1.y - p0.y);
    const b = Math.hypot(p2.x - p1.x, p2.y - p1.y);
    const c = Math.hypot(p2.x - p0.x, p2.y - p0.y);
    if (a < 1e-6 || b < 1e-6) {
      curvatures.push(0);
      continue;
    }
    const area2 = Math.abs((p1.x - p0.x) * (p2.y - p0.y) - (p1.y - p0.y) * (p2.x - p0.x));
    const kappa = (2 * area2) / (a * b * c + 1e-12);
    curvatures.push(kappa);
    maxCurvature = Math.max(maxCurvature, kappa);
  }
  const minBendRadius = maxCurvature > 1e-9 ? 1 / maxCurvature : Infinity;
  return { curvatures, maxCurvature, minBendRadius };
}

/**
 * Linear interpolation between two points.
 * @param {Point} a
 * @param {Point} b
 * @param {number} t
 * @returns {Point}
 */
export function lerpPoint(a, b, t) {
  return {
    x: a.x + (b.x - a.x) * t,
    y: a.y + (b.y - a.y) * t,
  };
}

/**
 * Horizontal spread of points near a given y level.
 * @param {Point[]} points
 * @param {number} targetY
 * @param {number} [tolerance=8]
 * @returns {number}
 */
function horizontalSpreadNearY(points, targetY, tolerance = 8) {
  const xs = points
    .filter((p) => Math.abs(p.y - targetY) <= tolerance)
    .map((p) => p.x);
  if (xs.length < 2) {
    const sorted = [...points].sort((a, b) => Math.abs(a.y - targetY) - Math.abs(b.y - targetY));
    const near = sorted.slice(0, Math.min(6, sorted.length));
    const xs2 = near.map((p) => p.x);
    return xs2.length >= 2 ? Math.max(...xs2) - Math.min(...xs2) : 0;
  }
  return Math.max(...xs) - Math.min(...xs);
}

/**
 * Flip profile if the narrower throat side is at the top so trachea (+y) points down.
 * @param {Point[]} points
 * @returns {Point[]}
 */
export function ensureTracheaDown(points) {
  if (points.length < 4) return points.map((p) => ({ ...p }));
  const maxY = Math.max(...points.map((p) => p.y));
  const minY = Math.min(...points.map((p) => p.y));
  const widthAtBottom = horizontalSpreadNearY(points, maxY);
  const widthAtTop = horizontalSpreadNearY(points, minY);
  // Throat is usually the narrower side; in our coords trachea should be at +y (down).
  if (widthAtTop < widthAtBottom * 0.85) {
    return points.map((p) => ({ x: p.x, y: -p.y }));
  }
  return points.map((p) => ({ ...p }));
}

/**
 * Arc length and point at the extreme y on a closed profile (max = trachea/ground, min = sky/back).
 * @param {Point[]} points
 * @param {'max' | 'min'} extreme
 * @returns {{ s: number, point: Point }}
 */
export function findArcLengthAtExtremeY(points, extreme = 'max') {
  const table = buildArcLengthTable(points);
  let bestY = extreme === 'max' ? -Infinity : Infinity;
  let bestS = 0;

  for (let i = 0; i < points.length; i++) {
    const a = points[i];
    const b = points[(i + 1) % points.length];
    const candidates = [
      { p: a, s: table.cumulative[i] },
      { p: b, s: table.cumulative[i + 1] },
      { p: { x: (a.x + b.x) / 2, y: (a.y + b.y) / 2 }, s: (table.cumulative[i] + table.cumulative[i + 1]) / 2 },
    ];
    for (const { p, s } of candidates) {
      if (extreme === 'max' ? p.y > bestY : p.y < bestY) {
        bestY = p.y;
        bestS = s;
      }
    }
  }

  return { s: bestS, point: getPointAtS(table, bestS) };
}

/**
 * Parse SVG viewBox string into components.
 * @param {string} viewBox
 * @returns {{ x: number, y: number, w: number, h: number }}
 */
export function parseViewBox(viewBox) {
  const [x, y, w, h] = viewBox.split(/\s+/).map(Number);
  return { x, y, w, h };
}

/**
 * Normalize points for SVG viewBox (center and scale to fit).
 * @param {Point[]} points
 * @param {number} padding
 * @returns {{ points: Point[], viewBox: string, scale: number, center: Point }}
 */
export function normalizeForView(points, padding = 40) {
  if (!points.length) return { points: [], viewBox: '0 0 400 400', scale: 1, center: { x: 0, y: 0 } };
  let minX = Infinity;
  let minY = Infinity;
  let maxX = -Infinity;
  let maxY = -Infinity;
  for (const p of points) {
    minX = Math.min(minX, p.x);
    minY = Math.min(minY, p.y);
    maxX = Math.max(maxX, p.x);
    maxY = Math.max(maxY, p.y);
  }
  const width = maxX - minX + padding * 2;
  const height = maxY - minY + padding * 2;
  const cx = (minX + maxX) / 2;
  const cy = (minY + maxY) / 2;
  return {
    points,
    viewBox: `${cx - width / 2} ${cy - height / 2} ${width} ${height}`,
    scale: Math.max(width, height),
    center: { x: cx, y: cy },
  };
}

/**
 * Convert points to SVG path d attribute.
 * @param {Point[]} points
 * @param {boolean} closed
 * @returns {string}
 */
export function pointsToSvgPath(points, closed = true) {
  if (!points.length) return '';
  const cmds = [`M ${points[0].x} ${points[0].y}`];
  for (let i = 1; i < points.length; i++) {
    cmds.push(`L ${points[i].x} ${points[i].y}`);
  }
  if (closed) cmds.push('Z');
  return cmds.join(' ');
}
