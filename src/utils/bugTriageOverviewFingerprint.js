/**
 * Stable short hash for localStorage keys derived from backlog overview fingerprint strings.
 * FNV-1a 32-bit — not for security, only deduplication.
 */
export function hashOverviewFingerprint(str) {
  if (typeof str !== 'string' || !str.length) return 'empty';
  let h = 0x811c9dc5;
  for (let i = 0; i < str.length; i++) {
    h ^= str.charCodeAt(i);
    h = Math.imul(h, 0x01000193);
  }
  return (h >>> 0).toString(16).padStart(8, '0');
}
