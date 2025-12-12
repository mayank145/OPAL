# OPAL Modernization Plan
## Subaru Telescope Observatory Management System

**Version:** 1.0  
**Date:** October 8, 2025  
**Current Status:** Legacy CGI Application (Python)  
**Target:** Modern, Secure, Industry-Standard Web Application

---

## Executive Summary

This document outlines a comprehensive plan to modernize the OPAL (Observatory Planning and Logging) system from a legacy CGI-based application to a modern, secure, maintainable web application following industry best practices.

**Timeline:** 6-9 months  
**Risk Level:** Current system has **CRITICAL** security vulnerabilities  
**Priority:** **URGENT** - Security fixes required immediately

---

## Table of Contents

1. [Current System Analysis](#1-current-system-analysis)
2. [Phase 0: Emergency Security Patches](#phase-0-emergency-security-patches-week-1-2)
3. [Phase 1: Planning & Setup](#phase-1-planning--setup-weeks-1-4)
4. [Phase 2: Backend Modernization](#phase-2-backend-modernization-weeks-5-12)
5. [Phase 3: Frontend Development](#phase-3-frontend-development-weeks-13-20)
6. [Phase 4: Testing & Migration](#phase-4-testing--migration-weeks-21-24)
7. [Phase 5: Deployment & Monitoring](#phase-5-deployment--monitoring-weeks-25-26)
8. [Post-Launch Support](#post-launch-support-ongoing)

---

## 1. Current System Analysis

### System Components (46 Python CGI Scripts)

#### A. Core Modules
- **Authentication:** login.py, login2.py, logout.py
- **Session Management:** logproc3.py (shared utilities)
- **Database:** Direct MySQL queries (SQL injection vulnerable)

#### B. Functional Areas

**1. Summit Logging System**
- `logone.py` - Daily log entry interface
- `loglist.py` - Log listing by year
- `itemone.py` - Individual log item management
- `itemsearch.py` - Log search functionality
- `sumcal.py` - Calendar view
- `logmail.py`, `mailam.py`, `mailpm.py` - Email notifications

**2. Car Reservation System**
- `resday.py` - Daily car overview
- `resone.py` - Individual reservation management
- `reslist.py` - Reservation listing
- `restimes.py`, `restimesOpen.py` - Real-time tracking
- `carcal.py` - Car calendar
- `carlist.py`, `carone.py` - Car management
- `blacklist.py`, `blackone.py` - Blackout management
- `shiftone.py`, `shifts.py` - Shift management

**3. User & Access Management**
- `userlist.py`, `userone.py` - User CRUD
- `ldaplist.py` - LDAP integration
- `starslist.py`, `starsone.py` - STARS user management
- `writeGroups.py` - LDAP sync utility

**4. Proposal & Program Management**
- `proplist.py`, `propone.py`, `propsmake.py` - Proposals
- `proglist.py`, `progone.py` - Programs
- `allocone.py` - Night allocations
- `planone.py` - Work plans

**5. Telescope Management**
- `tsrlist.py`, `tsrone.py`, `tsrmail.py` - TSR management

**6. Incident Tracking**
- `fatslist.py`, `fatsone.py`, `fatscomment.py` - FATS system

**7. Support Systems**
- `get_weather.py` - Weather monitoring
- `zoomlist.py` - Zoom meeting management

### Critical Issues Identified

#### Security (CRITICAL - P0)
- ❌ SQL Injection in ALL database queries
- ❌ No input validation/sanitization
- ❌ Weak session management (client-side cookies)
- ❌ No CSRF protection
- ❌ Plaintext password transmission
- ❌ No rate limiting
- ❌ Hardcoded credentials (admin users)
- ❌ No security headers

#### Architecture (HIGH - P1)
- ❌ CGI-based (deprecated technology)
- ❌ No separation of concerns (MVC)
- ❌ HTML mixed with business logic
- ❌ Massive code duplication
- ❌ No API layer
- ❌ Monolithic structure

#### Code Quality (MEDIUM - P2)
- ❌ No type hints
- ❌ No error handling
- ❌ Commented-out code everywhere
- ❌ Inconsistent coding standards
- ❌ No logging framework
- ❌ No unit tests

#### Operations (MEDIUM - P2)
- ❌ No containerization
- ❌ No CI/CD pipeline
- ❌ Manual deployment
- ❌ No monitoring/alerting
- ❌ No backup strategy documented

---

## Phase 0: Emergency Security Patches (Week 1-2)

**IMMEDIATE ACTION REQUIRED** - Mitigate critical vulnerabilities before full rewrite.

### Actions

#### 1. SQL Injection Mitigation (2-3 days)
**Priority:** CRITICAL  
**Assignee:** Backend Developer

Create a patch for all SQL queries:

```python
# BEFORE (VULNERABLE):
cursor.execute("SELECT * FROM users WHERE username='%s'" % username)

# AFTER (SECURE):
cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
```

**Files to patch:** ALL 46 Python files

#### 2. Input Validation Layer (1-2 days)
Create `validation.py` module:

```python
import re
from html import escape

def validate_username(username):
    if not re.match(r'^[a-zA-Z0-9_-]{3,30}$', username):
        raise ValueError("Invalid username")
    return escape(username)

def validate_email(email):
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        raise ValueError("Invalid email")
    return escape(email)

def validate_date(date_str):
    # ISO format validation
    if not re.match(r'^\d{4}-\d{2}-\d{2}$', date_str):
        raise ValueError("Invalid date format")
    return date_str
```

#### 3. Session Management Fix (1 day)
Replace client-side cookie storage with server-side sessions:

```python
import secrets
import shelve

def create_session(username):
    session_id = secrets.token_urlsafe(32)
    with shelve.open('sessions') as db:
        db[session_id] = {
            'username': username,
            'created': datetime.now(),
            'expires': datetime.now() + timedelta(hours=8)
        }
    return session_id
```

#### 4. HTTPS Enforcement (1 day)
- Add HTTPS redirect in Apache/Nginx config
- Obtain SSL certificate (Let's Encrypt)
- Update all internal URLs

#### 5. Security Headers (1 day)
Add to all responses:

```python
def add_security_headers():
    headers = {
        'X-Frame-Options': 'DENY',
        'X-Content-Type-Options': 'nosniff',
        'X-XSS-Protection': '1; mode=block',
        'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
        'Content-Security-Policy': "default-src 'self'"
    }
    return headers
```

#### 6. Rate Limiting (1 day)
Implement at web server level (Nginx):

```nginx
limit_req_zone $binary_remote_addr zone=login:10m rate=5r/m;
location /login.py {
    limit_req zone=login burst=10;
}
```

### Testing Emergency Patches
- [ ] SQL injection testing with sqlmap
- [ ] Session hijacking tests
- [ ] XSS vulnerability scanning
- [ ] Manual penetration testing
- [ ] Security audit with OWASP ZAP

### Deliverables
- Patched codebase with security fixes
- Security testing report
- Documentation of changes
- Rollback plan

---

## Phase 1: Planning & Setup (Weeks 1-4)

### Week 1-2: Requirements & Architecture

#### 1. Stakeholder Interviews
**Participants:** Astronomers, Support Staff, System Admins

**Questions:**
- Critical features vs nice-to-have?
- Pain points with current system?
- New feature requests?
- Integration requirements?
- Performance expectations?
- Mobile device usage?

#### 2. Technical Requirements Document (TRD)

**Template:**
```markdown
## Functional Requirements
- FR-001: User authentication via LDAP
- FR-002: Multi-tenant support (different crews)
- FR-003: Real-time car tracking
- [...]

## Non-Functional Requirements
- NFR-001: 99.9% uptime
- NFR-002: < 2s page load time
- NFR-003: Support 100 concurrent users
- NFR-004: WCAG 2.1 AA compliance
- [...]

## Integration Requirements
- INT-001: LDAP/Active Directory
- INT-002: Weather API integration
- INT-003: Email notifications (SMTP)
- INT-004: Zoom API
- [...]
```

#### 3. System Architecture Design

**Proposed Modern Architecture:**

```
┌─────────────────────────────────────────────────────────────┐
│                        Client Layer                          │
│  ┌─────────────────────────────────────────────────────┐   │
│  │   React SPA (TypeScript)                             │   │
│  │   - Redux for state management                       │   │
│  │   - Material-UI components                          │   │
│  │   - PWA capabilities                                │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            ↕ HTTPS/WSS
┌─────────────────────────────────────────────────────────────┐
│                     API Gateway Layer                        │
│  ┌─────────────────────────────────────────────────────┐   │
│  │   Nginx / Kong                                       │   │
│  │   - Rate limiting                                    │   │
│  │   - SSL termination                                  │   │
│  │   - Load balancing                                   │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            ↕ HTTP
┌─────────────────────────────────────────────────────────────┐
│                    Application Layer                         │
│  ┌──────────────────────────────────────────────────────┐  │
│  │   FastAPI Backend (Python 3.11+)                      │  │
│  │   ┌──────────────────────────────────────────────┐   │  │
│  │   │  REST API Endpoints                           │   │  │
│  │   │  - /api/v1/auth/                              │   │  │
│  │   │  - /api/v1/logs/                              │   │  │
│  │   │  - /api/v1/cars/                              │   │  │
│  │   │  - /api/v1/users/                             │   │  │
│  │   │  - /api/v1/proposals/                         │   │  │
│  │   │  - /api/v1/programs/                          │   │  │
│  │   │  - /api/v1/tsr/                               │   │  │
│  │   │  - /api/v1/fats/                              │   │  │
│  │   └──────────────────────────────────────────────┘   │  │
│  │   ┌──────────────────────────────────────────────┐   │  │
│  │   │  WebSocket Endpoints                          │   │  │
│  │   │  - Real-time car tracking                     │   │  │
│  │   │  - Live weather updates                       │   │  │
│  │   │  - Notification system                        │   │  │
│  │   └──────────────────────────────────────────────┘   │  │
│  │   ┌──────────────────────────────────────────────┐   │  │
│  │   │  Business Logic Layer                         │   │  │
│  │   │  - Domain models                              │   │  │
│  │   │  - Services                                   │   │  │
│  │   │  - Validators                                 │   │  │
│  │   └──────────────────────────────────────────────┘   │  │
│  │   ┌──────────────────────────────────────────────┐   │  │
│  │   │  Background Tasks (Celery)                    │   │  │
│  │   │  - Email notifications                        │   │  │
│  │   │  - Weather updates                            │   │  │
│  │   │  - Report generation                          │   │  │
│  │   │  - LDAP sync                                  │   │  │
│  │   └──────────────────────────────────────────────┘   │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            ↕ ORM
┌─────────────────────────────────────────────────────────────┐
│                      Data Layer                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │   PostgreSQL 15+                                      │  │
│  │   - Primary database                                  │  │
│  │   - Full-text search                                  │  │
│  │   - JSON fields for flexibility                       │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │   Redis                                               │  │
│  │   - Session storage                                   │  │
│  │   - Cache layer                                       │  │
│  │   - Celery message broker                            │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────────┐
│                  External Services                           │
│  - LDAP/Active Directory                                    │
│  - SMTP Server                                              │
│  - Weather APIs (Subaru/Keck)                              │
│  - Zoom API                                                 │
└─────────────────────────────────────────────────────────────┘
```

### Week 3: Technology Stack Selection

#### Backend Stack

**Framework:** FastAPI (Python 3.11+)
- ✅ Modern async support
- ✅ Automatic API documentation (OpenAPI/Swagger)
- ✅ Type hints with Pydantic validation
- ✅ High performance (Starlette + Uvicorn)
- ✅ WebSocket support
- ✅ Easy testing

**ORM:** SQLAlchemy 2.0
- ✅ Mature and well-documented
- ✅ Async support
- ✅ Migration management (Alembic)
- ✅ Query optimization

**Database:** PostgreSQL 15
- ✅ ACID compliance
- ✅ JSON support
- ✅ Full-text search
- ✅ Robust backup/recovery
- ✅ Better performance than MySQL for complex queries

**Caching:** Redis 7
- ✅ Session management
- ✅ Query caching
- ✅ Rate limiting
- ✅ Message broker for Celery

**Task Queue:** Celery
- ✅ Scheduled tasks
- ✅ Async email sending
- ✅ Background jobs
- ✅ Retry logic

**Authentication:** 
- OAuth2 with JWT tokens
- LDAP integration via python-ldap
- Multi-factor authentication (TOTP)

#### Frontend Stack

**Framework:** React 18 with TypeScript
- ✅ Component reusability
- ✅ Large ecosystem
- ✅ Type safety
- ✅ Strong community support

**State Management:** Redux Toolkit
- ✅ Predictable state
- ✅ DevTools
- ✅ Middleware support

**UI Framework:** Material-UI (MUI) v5
- ✅ Professional look
- ✅ Accessibility built-in
- ✅ Customizable themes
- ✅ Responsive design

**Data Fetching:** React Query
- ✅ Caching
- ✅ Background updates
- ✅ Optimistic updates
- ✅ Request deduplication

**Routing:** React Router v6
- ✅ Client-side routing
- ✅ Nested routes
- ✅ Code splitting

**Forms:** React Hook Form + Zod
- ✅ Performance
- ✅ Validation
- ✅ TypeScript integration

**Build Tool:** Vite
- ✅ Fast HMR
- ✅ Optimized builds
- ✅ Modern defaults

#### DevOps Stack

**Containerization:** Docker + Docker Compose
- ✅ Environment consistency
- ✅ Easy deployment
- ✅ Service isolation

**Orchestration:** Kubernetes (optional for production)
- ✅ Auto-scaling
- ✅ Self-healing
- ✅ Load balancing

**CI/CD:** GitHub Actions
- ✅ Automated testing
- ✅ Automated deployment
- ✅ Code quality checks

**Monitoring:** 
- Prometheus + Grafana (metrics)
- ELK Stack / Loki (logs)
- Sentry (error tracking)

**Testing:**
- pytest (backend unit/integration tests)
- Jest (frontend unit tests)
- Playwright (E2E tests)
- Locust (load testing)

### Week 4: Project Setup

#### 1. Repository Structure

```
opal-v2/
├── .github/
│   └── workflows/
│       ├── backend-ci.yml
│       ├── frontend-ci.yml
│       └── deploy.yml
├── backend/
│   ├── alembic/              # Database migrations
│   ├── app/
│   │   ├── api/
│   │   │   ├── v1/
│   │   │   │   ├── endpoints/
│   │   │   │   │   ├── auth.py
│   │   │   │   │   ├── logs.py
│   │   │   │   │   ├── cars.py
│   │   │   │   │   ├── users.py
│   │   │   │   │   ├── proposals.py
│   │   │   │   │   ├── programs.py
│   │   │   │   │   ├── tsr.py
│   │   │   │   │   └── fats.py
│   │   │   │   └── api.py
│   │   │   └── deps.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── security.py
│   │   │   └── logging.py
│   │   ├── db/
│   │   │   ├── base.py
│   │   │   └── session.py
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   ├── log.py
│   │   │   ├── car.py
│   │   │   ├── proposal.py
│   │   │   ├── program.py
│   │   │   ├── tsr.py
│   │   │   └── fats.py
│   │   ├── schemas/
│   │   │   ├── user.py
│   │   │   ├── log.py
│   │   │   ├── car.py
│   │   │   └── [...]
│   │   ├── services/
│   │   │   ├── auth.py
│   │   │   ├── log.py
│   │   │   ├── car.py
│   │   │   ├── email.py
│   │   │   ├── ldap.py
│   │   │   └── weather.py
│   │   ├── tasks/              # Celery tasks
│   │   │   ├── email.py
│   │   │   ├── weather.py
│   │   │   └── reports.py
│   │   ├── tests/
│   │   │   ├── api/
│   │   │   ├── services/
│   │   │   └── utils/
│   │   └── main.py
│   ├── scripts/
│   │   └── migrate_legacy_data.py
│   ├── .env.example
│   ├── Dockerfile
│   ├── poetry.lock
│   ├── pyproject.toml
│   └── requirements.txt
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── api/
│   │   │   └── client.ts
│   │   ├── components/
│   │   │   ├── common/
│   │   │   ├── logs/
│   │   │   ├── cars/
│   │   │   ├── users/
│   │   │   └── [...]
│   │   ├── features/
│   │   │   ├── auth/
│   │   │   ├── logs/
│   │   │   ├── cars/
│   │   │   └── [...]
│   │   ├── hooks/
│   │   ├── pages/
│   │   ├── store/
│   │   ├── types/
│   │   ├── utils/
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── .env.example
│   ├── Dockerfile
│   ├── package.json
│   ├── tsconfig.json
│   └── vite.config.ts
├── infrastructure/
│   ├── docker-compose.yml
│   ├── docker-compose.prod.yml
│   ├── nginx/
│   │   └── nginx.conf
│   └── kubernetes/          # If using K8s
│       ├── backend.yaml
│       ├── frontend.yaml
│       ├── postgres.yaml
│       └── redis.yaml
├── docs/
│   ├── api/
│   ├── architecture/
│   ├── deployment/
│   └── user-guide/
├── .gitignore
├── .pre-commit-config.yaml
├── Makefile
└── README.md
```

#### 2. Development Environment Setup

**Backend Setup:**

```bash
# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install poetry
poetry install

# Setup pre-commit hooks
pre-commit install

# Run tests
pytest

# Start development server
uvicorn app.main:app --reload
```

**Frontend Setup:**

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Run tests
npm run test

# Build for production
npm run build
```

**Docker Setup:**

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

#### 3. Database Schema Design

Modern schema with proper normalization:

```sql
-- Users and Authentication
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    stn_username VARCHAR(50),
    privilege VARCHAR(20) DEFAULT 'user',
    training_level VARCHAR(1) DEFAULT 'P',
    status VARCHAR(20) DEFAULT 'active',
    hour_in TIME DEFAULT '18:00',
    hour_out TIME DEFAULT '08:00',
    destiny VARCHAR(50) DEFAULT 'BHSB',
    shift_type VARCHAR(20) DEFAULT 'Daytime',
    shift_destination VARCHAR(50),
    shift_car VARCHAR(10),
    shift_date DATE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    deleted_at TIMESTAMP NULL
);

CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_status ON users(status);

-- Sessions
CREATE TABLE sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    token_hash VARCHAR(128) UNIQUE NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    ip_address INET,
    user_agent TEXT
);

CREATE INDEX idx_sessions_token ON sessions(token_hash);
CREATE INDEX idx_sessions_user ON sessions(user_id);

-- Summit Logs
CREATE TABLE days (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    date DATE UNIQUE NOT NULL,
    log_crew VARCHAR(10) NOT NULL,
    weather_conditions TEXT,
    crew_to VARCHAR(200),
    crew_io VARCHAR(200),
    crew_dc VARCHAR(200),
    mailed BOOLEAN DEFAULT FALSE,
    day_mailed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_days_date ON days(date);

-- Log Items
CREATE TABLE items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    day_id UUID REFERENCES days(id) ON DELETE CASCADE,
    date DATE NOT NULL,
    time TIME,
    crew VARCHAR(10),
    title VARCHAR(200),
    text TEXT,
    type VARCHAR(50),
    subsystem VARCHAR(50),
    downtime INTEGER DEFAULT 0,
    status VARCHAR(50),
    user_id UUID REFERENCES users(id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_items_date ON items(date);
CREATE INDEX idx_items_day ON items(day_id);
CREATE INDEX idx_items_user ON items(user_id);
CREATE INDEX idx_items_fulltext ON items USING GIN(to_tsvector('english', title || ' ' || text));

-- Cars
CREATE TABLE cars (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    car_name VARCHAR(20) UNIQUE NOT NULL,
    location VARCHAR(50),
    phone VARCHAR(20),
    passcode VARCHAR(10),
    type VARCHAR(30),
    sequence INTEGER,
    status VARCHAR(20) DEFAULT 'active',
    wheels VARCHAR(10),
    drivers TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Car Reservations
CREATE TABLE reservations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    car_id UUID REFERENCES cars(id),
    user_id UUID REFERENCES users(id),
    date DATE NOT NULL,
    time_out TIME,
    time_back TIME,
    destiny VARCHAR(50),
    passengers TEXT,
    status VARCHAR(20) DEFAULT 'pending',
    depart_time TIMESTAMP,
    arrive_time TIMESTAMP,
    return_depart_time TIMESTAMP,
    return_arrive_time TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    created_by UUID REFERENCES users(id),
    notes TEXT,
    CONSTRAINT no_overlap EXCLUDE USING gist (
        car_id WITH =,
        tsrange(
            (date + time_out)::timestamp,
            (date + time_back)::timestamp
        ) WITH &&
    )
);

CREATE INDEX idx_reservations_car ON reservations(car_id);
CREATE INDEX idx_reservations_user ON reservations(user_id);
CREATE INDEX idx_reservations_date ON reservations(date);

-- Blackout Periods
CREATE TABLE blackouts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    car_id UUID REFERENCES cars(id),
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    recurrence VARCHAR(20),
    type VARCHAR(50),
    warning TEXT,
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT NOW()
);

-- Proposals
CREATE TABLE proposals (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    prop_id VARCHAR(50) UNIQUE NOT NULL,
    semester_id VARCHAR(10),
    gid VARCHAR(50),
    instrument VARCHAR(50),
    pi_name VARCHAR(100),
    pi_email VARCHAR(100),
    date_in DATE,
    date_out DATE,
    support_astro VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_proposals_semester ON proposals(semester_id);
CREATE INDEX idx_proposals_gid ON proposals(gid);

-- Programs
CREATE TABLE programs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    day_id UUID REFERENCES days(id),
    date DATE NOT NULL,
    sequence INTEGER,
    instrument VARCHAR(50),
    allocation VARCHAR(20),
    pi_name VARCHAR(100),
    ao1 VARCHAR(100),
    ao2 VARCHAR(100),
    time_in TIME,
    time_out TIME,
    observers TEXT,
    support_scientist TEXT,
    gid VARCHAR(50),
    prop_id VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_programs_date ON programs(date);
CREATE INDEX idx_programs_prop_id ON programs(prop_id);

-- TSR (Telescope Setup Requests)
CREATE TABLE tsr (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    prop_id VARCHAR(50),
    gid VARCHAR(50),
    instrument VARCHAR(50),
    date DATE,
    pi_name VARCHAR(100),
    arrival_info TEXT,
    telescope_config JSONB,
    options JSONB,
    calibration_requirements TEXT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- FATS (Faults, Accidents, Troubles)
CREATE TABLE faults (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    date DATE NOT NULL,
    time TIME,
    section VARCHAR(50),
    title VARCHAR(200),
    description TEXT,
    solution TEXT,
    operator VARCHAR(100),
    status VARCHAR(20) DEFAULT 'open',
    todo TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    resolved_at TIMESTAMP
);

CREATE TABLE fault_comments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    fault_id UUID REFERENCES faults(id) ON DELETE CASCADE,
    comment TEXT,
    operator VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Weather Data
CREATE TABLE weather_readings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    timestamp TIMESTAMP NOT NULL,
    source VARCHAR(20),
    temperature DECIMAL(5,2),
    humidity INTEGER,
    alarm_status VARCHAR(20),
    alarm_text TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_weather_timestamp ON weather_readings(timestamp DESC);

-- Zoom Meetings
CREATE TABLE zoom_meetings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    date DATE NOT NULL,
    zoom_id VARCHAR(50),
    password VARCHAR(50),
    join_url TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Audit Log
CREATE TABLE audit_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    action VARCHAR(50) NOT NULL,
    table_name VARCHAR(50),
    record_id UUID,
    old_values JSONB,
    new_values JSONB,
    ip_address INET,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_audit_user ON audit_log(user_id);
CREATE INDEX idx_audit_created ON audit_log(created_at DESC);
```

---

## Phase 2: Backend Modernization (Weeks 5-12)

### Week 5-6: Core Infrastructure

#### 1. Configuration Management

**config.py:**

```python
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # App
    APP_NAME: str = "OPAL API"
    APP_VERSION: str = "2.0.0"
    DEBUG: bool = False
    
    # Database
    DATABASE_URL: str
    DB_POOL_SIZE: int = 5
    DB_MAX_OVERFLOW: int = 10
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    
    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 480
    
    # LDAP
    LDAP_SERVER: str
    LDAP_BASE_DN: str
    LDAP_BIND_DN: str
    LDAP_BIND_PASSWORD: str
    
    # Email
    SMTP_HOST: str
    SMTP_PORT: int = 587
    SMTP_USER: str
    SMTP_PASSWORD: str
    SMTP_FROM_EMAIL: str
    
    # External APIs
    WEATHER_API_URL: str
    WEATHER_API_FALLBACK: str
    ZOOM_API_KEY: str
    
    # Monitoring
    SENTRY_DSN: str | None = None
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    return Settings()
```

#### 2. Database Setup with SQLAlchemy

**db/base.py:**

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import get_settings

settings = get_settings()

engine = create_async_engine(
    settings.DATABASE_URL,
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    echo=settings.DEBUG,
)

async_session_maker = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

Base = declarative_base()

async def get_db() -> AsyncSession:
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
```

#### 3. Authentication System

**services/auth.py:**

```python
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import get_settings
from app.models.user import User
import secrets

settings = get_settings()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})
    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

async def authenticate_user(username: str, password: str, db):
    # First try LDAP
    user = await authenticate_ldap(username, password)
    if user:
        # Sync to local database
        await sync_ldap_user(user, db)
        return user
    
    # Fallback to local auth
    user = await db.get(User, username=username)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user
```

**services/ldap.py:**

```python
import ldap
from app.core.config import get_settings

settings = get_settings()

def authenticate_ldap(username: str, password: str) -> dict | None:
    try:
        conn = ldap.initialize(settings.LDAP_SERVER)
        conn.set_option(ldap.OPT_REFERRALS, 0)
        
        user_dn = f"uid={username},{settings.LDAP_BASE_DN}"
        conn.simple_bind_s(user_dn, password)
        
        # Fetch user details
        result = conn.search_s(
            settings.LDAP_BASE_DN,
            ldap.SCOPE_SUBTREE,
            f"(uid={username})",
            ['mail', 'cn', 'givenName', 'sn']
        )
        
        if result:
            _, attrs = result[0]
            return {
                'username': username,
                'email': attrs.get('mail', [b''])[0].decode(),
                'name': attrs.get('cn', [b''])[0].decode(),
            }
    except ldap.INVALID_CREDENTIALS:
        return None
    except Exception as e:
        logger.error(f"LDAP error: {e}")
        return None
    finally:
        conn.unbind_s()
    
    return None
```

### Week 7-8: API Endpoints - Part 1

#### Authentication Endpoints

**api/v1/endpoints/auth.py:**

```python
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.auth import Token, UserResponse
from app.services import auth

router = APIRouter()

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    user = await auth.authenticate_user(
        form_data.username,
        form_data.password,
        db
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = auth.create_access_token(
        data={"sub": user.username}
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.post("/logout")
async def logout(current_user = Depends(auth.get_current_user)):
    # Invalidate token (add to blacklist in Redis)
    await auth.invalidate_token(current_user)
    return {"message": "Successfully logged out"}

@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user = Depends(auth.get_current_user)):
    return current_user
```

#### Log Endpoints

**api/v1/endpoints/logs.py:**

```python
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID
from datetime import date

from app.db.session import get_db
from app.schemas.log import (
    LogDay,
    LogDayCreate,
    LogItem,
    LogItemCreate,
    LogItemUpdate
)
from app.services import log as log_service
from app.services.auth import get_current_user

router = APIRouter()

@router.get("/days/{date}", response_model=LogDay)
async def get_log_day(
    date: date,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    log_day = await log_service.get_day(db, date)
    if not log_day:
        raise HTTPException(status_code=404, detail="Log day not found")
    return log_day

@router.post("/days", response_model=LogDay)
async def create_log_day(
    log_day: LogDayCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return await log_service.create_day(db, log_day)

@router.get("/items/search", response_model=List[LogItem])
async def search_items(
    q: str = Query(..., min_length=3),
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return await log_service.search_items(db, q, skip, limit)

@router.post("/items", response_model=LogItem)
async def create_item(
    item: LogItemCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return await log_service.create_item(db, item, current_user.id)

@router.put("/items/{item_id}", response_model=LogItem)
async def update_item(
    item_id: UUID,
    item: LogItemUpdate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    updated = await log_service.update_item(db, item_id, item)
    if not updated:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated

@router.delete("/items/{item_id}")
async def delete_item(
    item_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    deleted = await log_service.delete_item(db, item_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted"}
```

#### Car Endpoints

**api/v1/endpoints/cars.py:**

```python
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID
from datetime import date, time

from app.db.session import get_db
from app.schemas.car import (
    Car,
    CarCreate,
    Reservation,
    ReservationCreate,
    ReservationUpdate,
    TimeUpdate
)
from app.services import car as car_service
from app.services.auth import get_current_user

router = APIRouter()

@router.get("", response_model=List[Car])
async def list_cars(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return await car_service.get_cars(db)

@router.get("/availability/{date}")
async def get_availability(
    date: date,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return await car_service.get_availability(db, date)

@router.post("/reservations", response_model=Reservation)
async def create_reservation(
    reservation: ReservationCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Check for conflicts
    conflicts = await car_service.check_conflicts(db, reservation)
    if conflicts:
        raise HTTPException(
            status_code=400,
            detail="Time slot conflicts with existing reservation"
        )
    
    # Create reservation
    new_reservation = await car_service.create_reservation(
        db,
        reservation,
        current_user.id
    )
    
    # Send email notification
    await car_service.send_reservation_email(new_reservation)
    
    return new_reservation

@router.put("/reservations/{reservation_id}/times")
async def update_times(
    reservation_id: UUID,
    times: TimeUpdate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    updated = await car_service.update_times(db, reservation_id, times)
    if not updated:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return updated

@router.get("/reservations/open")
async def get_open_reservations(
    db: AsyncSession = Depends(get_db)
):
    """Public endpoint for open reservations (no auth required)"""
    return await car_service.get_open_reservations(db)
```

### Week 9-10: API Endpoints - Part 2

Continue implementing endpoints for:
- Users (`/api/v1/users`)
- Proposals (`/api/v1/proposals`)
- Programs (`/api/v1/programs`)
- TSR (`/api/v1/tsr`)
- FATS (`/api/v1/fats`)
- Weather (`/api/v1/weather`)

### Week 11: Background Tasks

**tasks/email.py:**

```python
from celery import shared_task
from app.services.email import send_email

@shared_task
def send_log_summary(date: str):
    """Send daily summit log summary"""
    # Implementation
    pass

@shared_task
def send_reservation_notification(reservation_id: str):
    """Send car reservation notification"""
    # Implementation
    pass

@shared_task
def send_tsr_update(tsr_id: str):
    """Send TSR update email"""
    # Implementation
    pass
```

**tasks/weather.py:**

```python
from celery import shared_task
from app.services.weather import fetch_and_store_weather

@shared_task(bind=True, max_retries=3)
def update_weather(self):
    """Fetch weather data every 5 minutes"""
    try:
        fetch_and_store_weather()
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)
```

### Week 12: Testing & Documentation

#### Unit Tests

**tests/api/test_logs.py:**

```python
import pytest
from httpx import AsyncClient
from datetime import date

@pytest.mark.asyncio
async def test_create_log_item(client: AsyncClient, auth_headers):
    response = await client.post(
        "/api/v1/logs/items",
        json={
            "date": str(date.today()),
            "time": "10:30:00",
            "crew": "TO",
            "title": "Test item",
            "text": "Test description"
        },
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test item"

@pytest.mark.asyncio
async def test_search_items(client: AsyncClient, auth_headers):
    response = await client.get(
        "/api/v1/logs/items/search?q=test",
        headers=auth_headers
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)
```

#### API Documentation

FastAPI automatically generates OpenAPI docs at:
- `/docs` - Swagger UI
- `/redoc` - ReDoc

---

## Phase 3: Frontend Development (Weeks 13-20)

### Week 13-14: Foundation

#### 1. Setup React Project

```bash
npm create vite@latest frontend -- --template react-ts
cd frontend
npm install

# Install core dependencies
npm install @mui/material @emotion/react @emotion/styled
npm install @reduxjs/toolkit react-redux
npm install @tanstack/react-query
npm install react-router-dom
npm install react-hook-form zod @hookform/resolvers
npm install axios
npm install date-fns
npm install @mui/x-date-pickers
npm install @mui/x-data-grid
```

#### 2. API Client Setup

**src/api/client.ts:**

```typescript
import axios, { AxiosInstance } from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';

class APIClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Request interceptor - add auth token
    this.client.interceptors.request.use(
      (config) => {
        const token = localStorage.getItem('access_token');
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    // Response interceptor - handle errors
    this.client.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          // Token expired, redirect to login
          localStorage.removeItem('access_token');
          window.location.href = '/login';
        }
        return Promise.reject(error);
      }
    );
  }

  // Auth
  async login(username: string, password: string) {
    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);
    
    const response = await this.client.post('/auth/login', formData);
    return response.data;
  }

  async logout() {
    return this.client.post('/auth/logout');
  }

  async getCurrentUser() {
    const response = await this.client.get('/auth/me');
    return response.data;
  }

  // Logs
  async getLogDay(date: string) {
    const response = await this.client.get(`/logs/days/${date}`);
    return response.data;
  }

  async searchLogItems(query: string) {
    const response = await this.client.get(`/logs/items/search?q=${query}`);
    return response.data;
  }

  async createLogItem(data: any) {
    const response = await this.client.post('/logs/items', data);
    return response.data;
  }

  // Cars
  async getCars() {
    const response = await this.client.get('/cars');
    return response.data;
  }

  async getCarAvailability(date: string) {
    const response = await this.client.get(`/cars/availability/${date}`);
    return response.data;
  }

  async createReservation(data: any) {
    const response = await this.client.post('/cars/reservations', data);
    return response.data;
  }

  // Add more methods as needed...
}

export const apiClient = new APIClient();
```

#### 3. State Management

**src/store/store.ts:**

```typescript
import { configureStore } from '@reduxjs/toolkit';
import authReducer from '../features/auth/authSlice';
import uiReducer from '../features/ui/uiSlice';

export const store = configureStore({
  reducer: {
    auth: authReducer,
    ui: uiReducer,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
```

**src/features/auth/authSlice.ts:**

```typescript
import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface User {
  username: string;
  email: string;
  privilege: string;
}

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
}

const initialState: AuthState = {
  user: null,
  isAuthenticated: false,
  isLoading: true,
};

const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    setUser: (state, action: PayloadAction<User>) => {
      state.user = action.payload;
      state.isAuthenticated = true;
      state.isLoading = false;
    },
    clearUser: (state) => {
      state.user = null;
      state.isAuthenticated = false;
      state.isLoading = false;
    },
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.isLoading = action.payload;
    },
  },
});

export const { setUser, clearUser, setLoading } = authSlice.actions;
export default authSlice.reducer;
```

### Week 15-16: Core Pages

#### Login Page

**src/pages/LoginPage.tsx:**

```typescript
import React from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import {
  Box,
  Button,
  Container,
  TextField,
  Typography,
  Paper,
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { useDispatch } from 'react-redux';
import { apiClient } from '../api/client';
import { setUser } from '../features/auth/authSlice';

const loginSchema = z.object({
  username: z.string().min(3, 'Username must be at least 3 characters'),
  password: z.string().min(1, 'Password is required'),
});

type LoginFormData = z.infer<typeof loginSchema>;

export const LoginPage: React.FC = () => {
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
  });

  const onSubmit = async (data: LoginFormData) => {
    try {
      const response = await apiClient.login(data.username, data.password);
      localStorage.setItem('access_token', response.access_token);
      
      // Fetch user info
      const user = await apiClient.getCurrentUser();
      dispatch(setUser(user));
      
      navigate('/');
    } catch (error) {
      console.error('Login failed:', error);
      // Show error toast
    }
  };

  return (
    <Container maxWidth="sm">
      <Box sx={{ mt: 8, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
        <Paper elevation={3} sx={{ p: 4, width: '100%' }}>
          <Typography component="h1" variant="h4" align="center" gutterBottom>
            OPAL
          </Typography>
          <Typography variant="subtitle1" align="center" color="text.secondary" gutterBottom>
            Summit Calendar, Logs, Cars
          </Typography>
          
          <Box component="form" onSubmit={handleSubmit(onSubmit)} sx={{ mt: 3 }}>
            <TextField
              fullWidth
              label="Username"
              margin="normal"
              {...register('username')}
              error={!!errors.username}
              helperText={errors.username?.message}
            />
            <TextField
              fullWidth
              label="Password"
              type="password"
              margin="normal"
              {...register('password')}
              error={!!errors.password}
              helperText={errors.password?.message}
            />
            <Button
              type="submit"
              fullWidth
              variant="contained"
              size="large"
              sx={{ mt: 3 }}
              disabled={isSubmitting}
            >
              Login
            </Button>
          </Box>
        </Paper>
      </Box>
    </Container>
  );
};
```

#### Dashboard/Calendar

**src/pages/DashboardPage.tsx:**

```typescript
import React, { useState } from 'react';
import {
  Box,
  Container,
  Grid,
  Paper,
  Typography,
  Button,
  AppBar,
  Toolbar,
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { CalendarView } from '../components/logs/CalendarView';
import { WeatherWidget } from '../components/weather/WeatherWidget';
import { QuickActions } from '../components/common/QuickActions';

export const DashboardPage: React.FC = () => {
  const navigate = useNavigate();
  const [selectedDate, setSelectedDate] = useState(new Date());

  return (
    <Box>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            OPAL - Observatory Management
          </Typography>
          <Button color="inherit" onClick={() => navigate('/logout')}>
            Logout
          </Button>
        </Toolbar>
      </AppBar>

      <Container maxWidth="xl" sx={{ mt: 4 }}>
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <WeatherWidget />
          </Grid>

          <Grid item xs={12} md={9}>
            <Paper sx={{ p: 3 }}>
              <CalendarView
                selectedDate={selectedDate}
                onDateChange={setSelectedDate}
              />
            </Paper>
          </Grid>

          <Grid item xs={12} md={3}>
            <QuickActions />
          </Grid>
        </Grid>
      </Container>
    </Box>
  );
};
```

### Week 17-18: Feature Components

Implement components for:
- Summit Log Entry/Viewing
- Car Reservation System
- User Management
- Proposal Management
- TSR Management
- FATS System

### Week 19: Real-time Features

#### WebSocket Integration

**src/api/websocket.ts:**

```typescript
import { useEffect, useState } from 'react';

export const useWebSocket = (url: string) => {
  const [data, setData] = useState(null);
  const [isConnected, setIsConnected] = useState(false);

  useEffect(() => {
    const ws = new WebSocket(url);

    ws.onopen = () => {
      setIsConnected(true);
    };

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setData(data);
    };

    ws.onclose = () => {
      setIsConnected(false);
    };

    return () => {
      ws.close();
    };
  }, [url]);

  return { data, isConnected };
};

// Usage in component
export const LiveCarTracker: React.FC = () => {
  const { data, isConnected } = useWebSocket('ws://localhost:8000/ws/cars');

  return (
    <div>
      {isConnected ? 'Connected' : 'Disconnected'}
      {/* Render real-time data */}
    </div>
  );
};
```

### Week 20: Mobile Optimization & PWA

#### PWA Setup

**public/manifest.json:**

```json
{
  "name": "OPAL Observatory Management",
  "short_name": "OPAL",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#1976d2",
  "icons": [
    {
      "src": "/icon-192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "/icon-512.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ]
}
```

**Service Worker Registration:**

```typescript
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/sw.js');
  });
}
```

---

## Phase 4: Testing & Migration (Weeks 21-24)

### Week 21: Testing

#### Backend Testing

```python
# tests/api/test_integration.py
@pytest.mark.asyncio
async def test_full_reservation_flow(client, auth_headers, db):
    # Create car
    car = await create_test_car(db)
    
    # Create reservation
    response = await client.post(
        "/api/v1/cars/reservations",
        json={
            "car_id": str(car.id),
            "date": "2025-10-15",
            "time_out": "08:00:00",
            "time_back": "18:00:00",
            "destiny": "HP",
        },
        headers=auth_headers
    )
    assert response.status_code == 200
    
    # Update times
    reservation_id = response.json()["id"]
    response = await client.put(
        f"/api/v1/cars/reservations/{reservation_id}/times",
        json={"depart_time": "2025-10-15T08:05:00"},
        headers=auth_headers
    )
    assert response.status_code == 200
```

#### Frontend Testing

```typescript
// tests/components/LoginPage.test.tsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { LoginPage } from '../src/pages/LoginPage';

describe('LoginPage', () => {
  it('renders login form', () => {
    render(<LoginPage />);
    expect(screen.getByLabelText(/username/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
  });

  it('shows validation errors', async () => {
    render(<LoginPage />);
    
    const submitButton = screen.getByRole('button', { name: /login/i });
    fireEvent.click(submitButton);
    
    await waitFor(() => {
      expect(screen.getByText(/username must be at least 3 characters/i)).toBeInTheDocument();
    });
  });
});
```

#### E2E Testing

```typescript
// e2e/car-reservation.spec.ts
import { test, expect } from '@playwright/test';

test('complete car reservation flow', async ({ page }) => {
  // Login
  await page.goto('/login');
  await page.fill('input[name="username"]', 'testuser');
  await page.fill('input[name="password"]', 'password');
  await page.click('button[type="submit"]');

  // Navigate to car reservations
  await page.click('text=Cars');
  await page.click('text=Make Reservation');

  // Fill form
  await page.selectOption('select[name="car"]', 'J-01');
  await page.fill('input[name="date"]', '2025-10-15');
  await page.fill('input[name="time_out"]', '08:00');
  await page.fill('input[name="time_back"]', '18:00');

  // Submit
  await page.click('button:has-text("Submit")');

  // Verify success
  await expect(page.locator('text=Reservation created successfully')).toBeVisible();
});
```

#### Load Testing

```python
# locustfile.py
from locust import HttpUser, task, between

class OPALUser(HttpUser):
    wait_time = between(1, 3)
    
    def on_start(self):
        # Login
        response = self.client.post("/api/v1/auth/login", data={
            "username": "testuser",
            "password": "password"
        })
        self.token = response.json()["access_token"]
        self.client.headers = {"Authorization": f"Bearer {self.token}"}
    
    @task(3)
    def view_logs(self):
        self.client.get("/api/v1/logs/days/2025-10-15")
    
    @task(2)
    def search_items(self):
        self.client.get("/api/v1/logs/items/search?q=test")
    
    @task(1)
    def view_cars(self):
        self.client.get("/api/v1/cars/availability/2025-10-15")
```

### Week 22: Data Migration

#### Migration Script

**scripts/migrate_legacy_data.py:**

```python
import asyncio
import pymysql
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import async_session_maker
from app.models import User, Day, Item, Car, Reservation

async def migrate_users():
    """Migrate users from old to new database"""
    old_conn = pymysql.connect(
        host='localhost',
        user='old_user',
        password='old_password',
        db='sumlogs'
    )
    
    cursor = old_conn.cursor()
    cursor.execute("SELECT user, email, stnuser, privy, train, status FROM users")
    
    async with async_session_maker() as session:
        for row in cursor.fetchall():
            user = User(
                username=row[0].strip(),
                email=row[1].strip(),
                stn_username=row[2].strip(),
                privilege=row[3].strip(),
                training_level=row[4].strip(),
                status=row[5].strip()
            )
            session.add(user)
        
        await session.commit()
    
    old_conn.close()

async def migrate_days():
    """Migrate log days"""
    # Similar implementation
    pass

async def migrate_items():
    """Migrate log items"""
    pass

async def migrate_cars():
    """Migrate cars and reservations"""
    pass

async def migrate_all():
    print("Starting migration...")
    
    await migrate_users()
    print("✓ Users migrated")
    
    await migrate_days()
    print("✓ Days migrated")
    
    await migrate_items()
    print("✓ Items migrated")
    
    await migrate_cars()
    print("✓ Cars migrated")
    
    print("Migration complete!")

if __name__ == "__main__":
    asyncio.run(migrate_all())
```

### Week 23: User Acceptance Testing (UAT)

#### UAT Plan

1. **User Groups:**
   - Astronomers (observers)
   - Support staff
   - System administrators
   - Day crew
   - Night crew

2. **Test Scenarios:**
   - Daily log entry workflow
   - Car reservation workflow
   - Search functionality
   - TSR submission
   - FATS reporting
   - Weather monitoring
   - Mobile device usage

3. **Feedback Collection:**
   - Google Forms survey
   - Direct interviews
   - Bug tracking in GitHub Issues
   - Feature requests

4. **Acceptance Criteria:**
   - All critical features working
   - Performance acceptable (< 2s load time)
   - No show-stopper bugs
   - Positive user feedback

### Week 24: Bug Fixes & Polish

- Address UAT feedback
- Performance optimization
- UI/UX improvements
- Documentation updates

---

## Phase 5: Deployment & Monitoring (Weeks 25-26)

### Week 25: Production Deployment

#### Docker Compose Production

**docker-compose.prod.yml:**

```yaml
version: '3.8'

services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./infrastructure/nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./frontend/dist:/usr/share/nginx/html:ro
      - /etc/letsencrypt:/etc/letsencrypt:ro
    depends_on:
      - backend
    restart: unless-stopped

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    environment:
      - DATABASE_URL=postgresql+asyncpg://opal:${DB_PASSWORD}@postgres:5432/opal
      - REDIS_URL=redis://redis:6379
      - SECRET_KEY=${SECRET_KEY}
    depends_on:
      - postgres
      - redis
    restart: unless-stopped
    deploy:
      replicas: 3

  celery-worker:
    build: ./backend
    command: celery -A app.tasks worker --loglevel=info
    environment:
      - DATABASE_URL=postgresql+asyncpg://opal:${DB_PASSWORD}@postgres:5432/opal
      - REDIS_URL=redis://redis:6379
    depends_on:
      - postgres
      - redis
    restart: unless-stopped

  celery-beat:
    build: ./backend
    command: celery -A app.tasks beat --loglevel=info
    environment:
      - DATABASE_URL=postgresql+asyncpg://opal:${DB_PASSWORD}@postgres:5432/opal
      - REDIS_URL=redis://redis:6379
    depends_on:
      - postgres
      - redis
    restart: unless-stopped

  postgres:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=opal
      - POSTGRES_PASSWORD=${DB_PASSWORD}
      - POSTGRES_DB=opal
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./backups:/backups
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
```

#### Deployment Script

**scripts/deploy.sh:**

```bash
#!/bin/bash
set -e

echo "Deploying OPAL v2..."

# Pull latest code
git pull origin main

# Build frontend
cd frontend
npm install
npm run build
cd ..

# Build and start containers
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml up -d

# Run migrations
docker-compose -f docker-compose.prod.yml exec backend alembic upgrade head

# Health check
sleep 10
curl -f http://localhost/api/health || exit 1

echo "✓ Deployment complete!"
```

#### CI/CD Pipeline

**.github/workflows/deploy.yml:**

```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Backend Tests
        run: |
          cd backend
          pip install -r requirements.txt
          pytest
      
      - name: Frontend Tests
        run: |
          cd frontend
          npm install
          npm run test

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Deploy to Production
        uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.PROD_HOST }}
          username: ${{ secrets.PROD_USER }}
          key: ${{ secrets.SSH_PRIVATE_KEY }}
          script: |
            cd /opt/opal
            ./scripts/deploy.sh
```

### Week 26: Monitoring Setup

#### Prometheus Configuration

**infrastructure/prometheus/prometheus.yml:**

```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'opal-backend'
    static_configs:
      - targets: ['backend:8000']

  - job_name: 'postgres'
    static_configs:
      - targets: ['postgres:5432']

  - job_name: 'redis'
    static_configs:
      - targets: ['redis:6379']
```

#### Grafana Dashboards

Create dashboards for:
- Request rate and latency
- Database performance
- Cache hit rate
- Error rate
- Active users
- Resource usage (CPU, memory)

#### Logging Setup

**backend/app/core/logging.py:**

```python
import logging
import sys
from loguru import logger

def setup_logging():
    # Remove default handler
    logger.remove()
    
    # Add custom handlers
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level="INFO"
    )
    
    logger.add(
        "/var/log/opal/app.log",
        rotation="500 MB",
        retention="10 days",
        compression="zip",
        level="INFO"
    )
    
    logger.add(
        "/var/log/opal/error.log",
        rotation="100 MB",
        retention="30 days",
        level="ERROR"
    )
```

#### Error Tracking (Sentry)

```python
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration

sentry_sdk.init(
    dsn=settings.SENTRY_DSN,
    integrations=[FastApiIntegration()],
    traces_sample_rate=0.1,
    environment="production"
)
```

---

## Post-Launch Support (Ongoing)

### Week 27-30: Stabilization Period

- 24/7 monitoring
- Rapid bug fixes
- User support
- Performance tuning
- Documentation improvements

### Maintenance Plan

#### Daily Tasks
- Monitor error logs
- Check system health
- Review user feedback

#### Weekly Tasks
- Database backup verification
- Security updates
- Performance review
- User feedback analysis

#### Monthly Tasks
- Security audit
- Dependency updates
- Database optimization
- Capacity planning

#### Quarterly Tasks
- Major feature releases
- Comprehensive security review
- Disaster recovery drill
- User satisfaction survey

### Support Structure

**Support Tiers:**

1. **Tier 1 - Users:**
   - Self-service documentation
   - FAQ
   - Email support

2. **Tier 2 - Support Staff:**
   - Ticket system
   - Direct email to dev team
   - Slack channel

3. **Tier 3 - Critical Issues:**
   - On-call rotation
   - Direct phone support
   - Emergency response

---

## Success Metrics

### Technical Metrics
- [ ] 99.9% uptime
- [ ] < 2s average page load time
- [ ] < 100ms API response time (95th percentile)
- [ ] Zero critical security vulnerabilities
- [ ] 80%+ code coverage
- [ ] < 5 production bugs per month

### User Metrics
- [ ] 90%+ user satisfaction
- [ ] 100% feature parity with legacy system
- [ ] < 1 hour training time for new users
- [ ] 50%+ reduction in support tickets
- [ ] Mobile usage > 30%

### Business Metrics
- [ ] Reduced maintenance costs (50%)
- [ ] Improved observatory operations efficiency
- [ ] Better data insights
- [ ] Reduced downtime

---

## Risk Management

### Technical Risks

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| Data migration issues | Medium | High | Extensive testing, rollback plan |
| Performance problems | Low | Medium | Load testing, caching strategy |
| Integration failures (LDAP) | Medium | High | Fallback authentication, thorough testing |
| Security breaches | Low | Critical | Security audits, penetration testing |
| Downtime during migration | Medium | High | Parallel running, gradual rollout |

### Project Risks

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| Timeline delays | Medium | Medium | Buffer time, phased approach |
| Scope creep | High | Medium | Strict change management |
| User resistance | Medium | High | Early involvement, training |
| Resource unavailability | Low | High | Cross-training, documentation |

---

## Budget Estimate

### Development Costs
- **Backend Developer** (3 months full-time): $45,000
- **Frontend Developer** (3 months full-time): $45,000
- **DevOps Engineer** (1 month full-time): $15,000
- **QA Engineer** (1 month full-time): $12,000
- **Total Development:** $117,000

### Infrastructure Costs (Annual)
- **Cloud hosting** (VPS/Cloud): $2,400
- **Database hosting**: Included
- **SSL certificates**: Free (Let's Encrypt)
- **Monitoring tools**: $1,200
- **Backup storage**: $600
- **Total Infrastructure:** $4,200/year

### One-time Costs
- **Security audit**: $5,000
- **Training materials**: $2,000
- **Documentation**: $3,000
- **Total One-time:** $10,000

### **Grand Total:** $131,200 (first year)

---

## Conclusion

This modernization plan transforms OPAL from a legacy CGI application into a modern, secure, maintainable web application following industry best practices. The phased approach allows for:

1. **Immediate security fixes** to protect current operations
2. **Gradual migration** to minimize disruption
3. **Thorough testing** to ensure reliability
4. **User involvement** to ensure adoption
5. **Sustainable architecture** for future growth

The new system will provide:
- ✅ Enhanced security
- ✅ Better performance
- ✅ Improved user experience
- ✅ Mobile access
- ✅ Real-time updates
- ✅ Easier maintenance
- ✅ Better scalability

**Recommended Next Steps:**
1. Review and approve this plan
2. Assemble development team
3. Begin Phase 0 (Emergency Security Patches) immediately
4. Schedule kickoff meeting for Phase 1

