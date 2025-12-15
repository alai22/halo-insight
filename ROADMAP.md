# Halo Insight - Product Roadmap

## Overview
Halo Insight is an AI-powered customer intelligence platform that analyzes feedback across Gladly (support conversations), Survicate (churn surveys), and Zoom (chat interactions). This roadmap outlines the evolution from a multi-bot architecture to a unified, user-centric platform.

---

## Phase 1: Authentication & User Management (Q1)

### 1.1 Enhanced Authentication
**Status:** Basic magic link exists, needs enhancement

**Tasks:**
- [ ] **Google OAuth Integration**
  - Implement Google Sign-In with OAuth 2.0
  - Support `@halocollar.com` domain restriction
  - Store user profile (name, email, avatar) in database
  
- [ ] **Email Magic Link Enhancement**
  - Improve email delivery reliability (currently using EmailService)
  - Add email templates with branding
  - Implement rate limiting for magic link requests
  - Add expiration tracking and cleanup

- [ ] **Session Management**
  - Migrate from in-memory sessions to database-backed sessions
  - Implement refresh tokens for long-lived sessions
  - Add device tracking and session revocation

**Deliverables:**
- Users can sign in via Google OAuth or email magic link
- Secure session management with database persistence
- Admin dashboard for user management

---

## Phase 2: Database & User Data (Q1-Q2)

### 2.1 Relational Database Setup
**Status:** Currently using in-memory storage and S3

**Tasks:**
- [ ] **Database Selection & Setup**
  - Choose database (PostgreSQL recommended for production)
  - Set up database schema with migrations (Alembic/Flyway)
  - Configure connection pooling and backups
  
- [ ] **User Schema**
  ```sql
  - users (id, email, name, avatar_url, created_at, last_login)
  - user_sessions (id, user_id, token, expires_at, device_info)
  - user_preferences (user_id, preferences_json)
  - user_roles (user_id, role, permissions)
  ```

- [ ] **Data Source Connections**
  ```sql
  - data_source_connections (id, user_id, source_type, credentials_encrypted, status, last_sync)
  - sync_history (id, connection_id, sync_type, records_count, status, error_message, synced_at)
  ```

**Deliverables:**
- PostgreSQL database with user and data source schemas
- Migration scripts for schema versioning
- Database connection pooling and health checks

### 2.2 User-Level Data Storage
**Tasks:**
- [ ] **User Data Isolation**
  - Store conversation/survey/zoom data per user
  - Implement row-level security or application-level filtering
  - Add data retention policies per user
  
- [ ] **User Preferences**
  - Save user dashboard preferences (filters, views, date ranges)
  - Store favorite queries and saved searches
  - Remember data source selections

- [ ] **User Activity Tracking**
  - Log user queries and interactions
  - Track feature usage for analytics
  - Store conversation history per user

**Deliverables:**
- Multi-tenant data architecture
- User preferences persistence
- Activity logging system

---

## Phase 3: Learn & Onboarding Integration (Q2)

### 3.1 Learn Platform Connection
**Status:** Not currently integrated

**Tasks:**
- [ ] **Learn API Integration**
  - Identify Learn platform API (if available) or database connection
  - Map user completion data structure
  - Create data sync service for Learn completion records
  
- [ ] **Onboarding Data Model**
  ```sql
  - learn_completions (id, user_id, course_id, lesson_id, completed_at, score, time_spent)
  - onboarding_steps (id, user_id, step_name, completed_at, data_json)
  - user_onboarding_status (user_id, current_step, completion_percentage, started_at, completed_at)
  ```

- [ ] **Data Sync Service**
  - Periodic sync job for Learn completion data
  - Real-time webhook support (if Learn platform supports)
  - Error handling and retry logic

**Deliverables:**
- Learn completion data in database
- Onboarding progress tracking
- API endpoints for querying Learn data

### 3.2 Onboarding Flow
**Tasks:**
- [ ] **First-Time User Experience**
  - Welcome screen with platform overview
  - Guided tour of key features
  - Data source connection wizard
  
- [ ] **Onboarding Completion Tracking**
  - Track completion of onboarding steps
  - Show progress indicator
  - Unlock features based on completion status

- [ ] **User Education**
  - Interactive tutorials for each data source
  - Best practices for querying data
  - Example queries and use cases

**Deliverables:**
- Complete onboarding flow
- Progress tracking UI
- User education materials

---

## Phase 4: Zoom API Enhancement (Q2-Q3)

### 4.1 Zoom Data Integration
**Status:** Basic Zoom download exists (`zoom_routes.py`, `ZoomDownloadService`)

**Tasks:**
- [ ] **Zoom API Connection**
  - Verify current Zoom OAuth implementation (`ZoomAPIClient`)
  - Enhance error handling and retry logic
  - Add support for additional Zoom data types (meetings, recordings, transcripts)
  
- [ ] **Data Normalization**
  - Standardize Zoom chat message format
  - Map Zoom data to unified conversation schema
  - Handle different Zoom message types (chat, Q&A, polls)

- [ ] **Real-Time Sync**
  - Webhook support for real-time Zoom updates
  - Incremental sync instead of full downloads
  - Background job for periodic syncs

**Deliverables:**
- Robust Zoom API integration
- Normalized Zoom data in database
- Real-time sync capabilities

### 4.2 Zoom Analytics
**Tasks:**
- [ ] **Zoom-Specific Analytics**
  - Chat volume trends
  - Response time metrics
  - Topic extraction from Zoom chats
  - Integration with existing analytics dashboard

**Deliverables:**
- Zoom analytics in dashboard
- Cross-source analytics (Gladly + Zoom + Survicate)

---

## Phase 5: Unified Bot Architecture (Q3-Q4)

### 5.1 Current State Analysis
**Status:** Three separate RAG services exist:
- `RAGService` (Gladly conversations)
- `SurvicateRAGService` (Survicate surveys)  
- Zoom RAG (needs implementation)

**Tasks:**
- [ ] **Unified Data Schema**
  - Create common data model across all sources
  - Map Gladly conversations → unified format
  - Map Survicate surveys → unified format
  - Map Zoom chats → unified format
  
- [ ] **Unified RAG Service**
  - Merge three RAG services into `UnifiedRAGService`
  - Single query interface that searches all sources
  - Intelligent source selection based on query intent
  - Cross-source relationship detection

- [ ] **Query Router**
  - Analyze query to determine relevant data sources
  - Route to appropriate sources or all sources
  - Aggregate results from multiple sources
  - Provide source attribution in responses

**Deliverables:**
- Single unified bot interface
- Cross-source querying capability
- Unified response format

### 5.2 Advanced Unified Features
**Tasks:**
- [ ] **Cross-Source Insights**
  - Identify patterns across Gladly, Survicate, and Zoom
  - Connect customer journey across touchpoints
  - Detect correlations between support issues and churn reasons
  
- [ ] **Contextual Understanding**
  - Understand customer context across all interactions
  - Track customer journey timeline
  - Provide holistic customer view

- [ ] **Unified Analytics**
  - Combined analytics dashboard
  - Cross-source trend analysis
  - Unified reporting

**Deliverables:**
- Cross-source intelligence
- Customer journey mapping
- Unified analytics dashboard

---

## Phase 6: Platform Enhancements (Q4)

### 6.1 Performance & Scalability
**Tasks:**
- [ ] **Caching Layer**
  - Redis for query result caching
  - Cache frequently accessed data
  - Implement cache invalidation strategies
  
- [ ] **Query Optimization**
  - Optimize database queries
  - Implement pagination for large result sets
  - Add query result streaming for long-running queries

- [ ] **Background Jobs**
  - Celery or similar for async tasks
  - Queue system for data syncs
  - Scheduled jobs for analytics updates

**Deliverables:**
- Improved query performance
- Scalable architecture
- Background job system

### 6.2 Advanced Features
**Tasks:**
- [ ] **Custom Dashboards**
  - User-configurable dashboards
  - Drag-and-drop widget builder
  - Shareable dashboard templates
  
- [ ] **Alerts & Notifications**
  - Set up alerts for specific query patterns
  - Email/Slack notifications for insights
  - Real-time alert system

- [ ] **Export & Reporting**
  - Export queries to PDF/Excel
  - Scheduled report generation
  - Custom report templates

**Deliverables:**
- Custom dashboard builder
- Alert system
- Advanced reporting

---

## Technical Architecture Decisions

### Database
- **Recommendation:** PostgreSQL
- **ORM:** SQLAlchemy (already in use)
- **Migrations:** Alembic

### Authentication
- **Google OAuth:** `google-auth` + `google-auth-oauthlib`
- **Session Storage:** Database-backed sessions (Flask-Session)
- **Token Management:** JWT for API access, refresh tokens for long sessions

### Background Jobs
- **Recommendation:** Celery with Redis broker
- **Alternative:** RQ (simpler, Redis-based)

### Caching
- **Recommendation:** Redis
- **Use Cases:** Query results, user sessions, frequently accessed data

### Data Sync
- **Pattern:** Periodic sync jobs + webhooks (where available)
- **Error Handling:** Retry with exponential backoff
- **Monitoring:** Log sync status and errors

---

## Success Metrics

### Phase 1 (Auth)
- 100% of users can authenticate via Google or email
- Zero session-related errors
- <2 second authentication time

### Phase 2 (Database)
- All user data persisted in database
- Zero data loss incidents
- <100ms average query response time

### Phase 3 (Learn)
- 100% of Learn completion data synced
- Onboarding completion rate >80%
- User activation time <10 minutes

### Phase 4 (Zoom)
- 100% of Zoom chats accessible
- Real-time sync latency <5 minutes
- Zero data sync failures

### Phase 5 (Unified Bot)
- 90% of queries use unified bot
- Cross-source insights identified automatically
- Query response time <5 seconds

### Phase 6 (Platform)
- 99.9% uptime
- Dashboard load time <2 seconds
- User satisfaction score >4.5/5

---

## Dependencies & Prerequisites

### External Services
- Google OAuth credentials
- Learn platform API access or database connection
- Zoom API credentials (already configured)
- PostgreSQL database instance
- Redis instance (for caching/jobs)

### Team Requirements
- Backend developer (Python/Flask)
- Frontend developer (React)
- Database administrator
- DevOps engineer (for infrastructure)

### Infrastructure
- Database hosting (AWS RDS, managed PostgreSQL)
- Redis hosting (AWS ElastiCache, managed Redis)
- Background job workers (EC2, ECS, or Lambda)

---

## Risk Mitigation

### Data Migration
- **Risk:** Migrating from S3/in-memory to database
- **Mitigation:** Gradual migration with dual-write period, comprehensive testing

### Unified Bot Complexity
- **Risk:** Merging three specialized bots may reduce quality
- **Mitigation:** A/B testing, gradual rollout, fallback to specialized bots

### Performance
- **Risk:** Unified queries may be slower
- **Mitigation:** Caching, query optimization, parallel processing

### User Adoption
- **Risk:** Users may prefer specialized bots
- **Mitigation:** User research, gradual transition, maintain specialized bots as option

---

## Timeline Summary

| Phase | Duration | Key Deliverables |
|-------|----------|------------------|
| Phase 1: Auth | Q1 (3 months) | Google OAuth, Enhanced magic link |
| Phase 2: Database | Q1-Q2 (4 months) | PostgreSQL setup, User data storage |
| Phase 3: Learn | Q2 (3 months) | Learn integration, Onboarding flow |
| Phase 4: Zoom | Q2-Q3 (3 months) | Enhanced Zoom API, Real-time sync |
| Phase 5: Unified Bot | Q3-Q4 (4 months) | Unified RAG service, Cross-source insights |
| Phase 6: Platform | Q4 (3 months) | Performance, Advanced features |

**Total Timeline:** ~12-15 months for complete roadmap

---

## Next Steps

1. **Immediate (Week 1-2)**
   - Set up PostgreSQL database
   - Create database schema and migrations
   - Begin Google OAuth implementation

2. **Short-term (Month 1-2)**
   - Complete authentication enhancements
   - Migrate user data to database
   - Start Learn API research

3. **Medium-term (Month 3-6)**
   - Complete Learn integration
   - Enhance Zoom API
   - Begin unified bot architecture design

4. **Long-term (Month 7-12)**
   - Implement unified bot
   - Platform enhancements
   - Performance optimization

---

*Last Updated: [Current Date]*
*Version: 1.0*



