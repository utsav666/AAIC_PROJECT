# Dyslexia Learning Platform - Architecture & Flow

## High-Level System Architecture

```mermaid
graph TB
    subgraph Client["Frontend (React/Next.js)"]
        UI[Dyslexia-Friendly UI]
        GameEngine[Gamification Engine]
        TTS[Text-to-Speech Module]
        MultiSensory[Multi-Sensory Input Handler]
    end

    subgraph Auth["Authentication Layer"]
        Login[Login/Register]
        OAuth[OAuth2 Provider]
        Session[Session Manager]
    end

    subgraph API["Backend API (FastAPI)"]
        UserSvc[User Service]
        AssessmentSvc[Assessment Service]
        LevelSvc[Level Management Service]
        ProgressSvc[Progress Tracking Service]
        ContentSvc[Content Delivery Service]
        NotifSvc[Notification Service]
    end

    subgraph AI["AI/ML Layer"]
        AssessmentAI[Assessment AI Model]
        AdaptiveAI[Adaptive Learning AI]
        ProgressAI[Progress Prediction AI]
        NLP[NLP Engine]
    end

    subgraph Data["Data Layer"]
        PG[(PostgreSQL)]
        Redis[(Redis Cache)]
        S3[Content Storage]
    end

    subgraph External["External Services"]
        OpenAI[OpenAI API]
        Analytics[Analytics Engine]
        ParentDash[Parent/Teacher Dashboard]
    end

    UI --> Login
    Login --> OAuth
    OAuth --> Session
    Session --> API

    UI --> AssessmentSvc
    UI --> ContentSvc
    GameEngine --> ProgressSvc

    AssessmentSvc --> AssessmentAI
    LevelSvc --> AdaptiveAI
    ProgressSvc --> ProgressAI
    AssessmentAI --> NLP
    NLP --> OpenAI

    UserSvc --> PG
    AssessmentSvc --> PG
    LevelSvc --> PG
    ProgressSvc --> PG
    ContentSvc --> S3
    Session --> Redis

    ProgressSvc --> Analytics
    Analytics --> ParentDash
    NotifSvc --> ParentDash
```

## User Journey Flow (Connected Phases)

```mermaid
flowchart TD
    %% Phase 1: Onboarding
    subgraph P1["🟦 Phase 1: Onboarding"]
        direction TB
        A[👤 Register] --> B[Parent Account]
        B --> C[Child Profile]
        C --> D{First Time?}
    end

    %% Phase 2: Assessment
    subgraph P2["🟩 Phase 2: AI Assessment"]
        E[🧪 Assessment Test]
        E --> T1[Phonemic Awareness]
        E --> T2[Letter Recognition]
        E --> T3[Reading Speed]
        E --> T4[Comprehension]
        E --> T5[Visual Processing]
        T1 & T2 & T3 & T4 & T5 --> G[🤖 AI Scoring]
        G --> H{Classification}
        H -->|Mild| L12[Level 1-2]
        H -->|Moderate| L34[Level 3-4]
        H -->|Severe| L5[Level 5]
        L12 & L34 & L5 --> PATH[📚 Learning Path Created]
    end

    %% Phase 3: Daily Learning
    subgraph P3["🟨 Phase 3: Daily Learning Loop"]
        direction LR
        SESSION[📖 Session] --> ACT[Activity] --> EVAL{🤖 Pass?}
        EVAL -->|Yes| NEXT[Next Module]
        EVAL -->|No| SESSION
        NEXT --> DONE{Level Done?}
    end

    %% Phase 3 AI Support
    subgraph P3AI["🧠 AI in Learning"]
        direction LR
        ADAPT[Adaptive Difficulty]
        HINT[Smart Hints]
        STYLE[Learning Style Switch]
    end

    %% Phase 4: Progression
    subgraph P4["🟥 Phase 4: Level Progression"]
        REASSESS[🧪 Re-Assessment] --> DECIDE{Promote?}
        DECIDE -->|Yes ⬆️| UP[Next Level]
        DECIDE -->|No 🔁| STAY[Reinforce]
    end

    %% Phase 4 AI Support
    subgraph P4AI["🧠 AI in Progression"]
        direction LR
        PREDICT[Readiness Prediction]
        GAP[Gap Analysis]
        REPORT[Parent Insights]
    end

    %% AI connections
    EVAL -.->|feeds| P3AI
    P3AI -.->|adjusts| ACT
    REASSESS -.->|uses| P4AI
    P4AI -.->|informs| DECIDE

    %% Connections between phases
    D -->|Yes| E
    D -->|No| SESSION
    PATH --> SESSION
    DONE -->|Yes| REASSESS
    UP --> SESSION
    STAY --> SESSION
```

## Assessment Engine Detail

```mermaid
flowchart LR
    subgraph Input["Test Input"]
        A1[Audio Response]
        A2[Touch/Click Response]
        A3[Written Response]
        A4[Timing Data]
    end

    subgraph Processing["AI Processing Pipeline"]
        B1[Speech-to-Text]
        B2[Pattern Recognition]
        B3[Error Classification]
        B4[Response Time Analysis]
        B5[Confidence Scoring]
    end

    subgraph Classification["Level Classification Model"]
        C1[Feature Extraction]
        C2[Dyslexia Type Detection]
        C3[Severity Scoring]
        C4[Level Assignment]
    end

    subgraph Output["Assessment Output"]
        D1[Level: L1-L5]
        D2[Dyslexia Profile]
        D3[Recommended Path]
        D4[Parent Report]
    end

    A1 --> B1
    A2 --> B2
    A3 --> B3
    A4 --> B4
    
    B1 & B2 & B3 & B4 --> B5
    B5 --> C1
    C1 --> C2
    C2 --> C3
    C3 --> C4
    
    C4 --> D1
    C2 --> D2
    C4 --> D3
    C3 --> D4
```

## Progress Tracking & Adaptive AI

```mermaid
flowchart TD
    subgraph Tracking["Progress Data Collection"]
        T1[Accuracy per Module]
        T2[Time Spent]
        T3[Error Patterns]
        T4[Retry Count]
        T5[Engagement Score]
    end

    subgraph AIEngine["AI Progress Engine"]
        AI1[Trend Analysis]
        AI2[Plateau Detection]
        AI3[Strength/Weakness Map]
        AI4[Pace Optimization]
    end

    subgraph Actions["Adaptive Actions"]
        ACT1[Adjust Difficulty]
        ACT2[Switch Learning Strategy]
        ACT3[Recommend Break]
        ACT4[Celebrate Achievement]
        ACT5[Alert Parent/Teacher]
        ACT6[Suggest Re-Assessment]
    end

    T1 & T2 & T3 & T4 & T5 --> AI1
    AI1 --> AI2
    AI1 --> AI3
    AI2 --> AI4
    AI3 --> AI4

    AI4 --> ACT1
    AI2 --> ACT2
    AI2 --> ACT3
    AI3 --> ACT4
    AI2 --> ACT5
    AI4 --> ACT6
```

## Level & Module Structure

```mermaid
graph TD
    subgraph L1["Level 1 - Foundation"]
        L1M1[Letter Recognition]
        L1M2[Basic Phonics]
        L1M3[Letter-Sound Mapping]
        L1M4[Simple CVC Words]
    end

    subgraph L2["Level 2 - Building Blocks"]
        L2M1[Blends & Digraphs]
        L2M2[Sight Words Set 1]
        L2M3[Short Sentences]
        L2M4[Rhyming Patterns]
    end

    subgraph L3["Level 3 - Developing"]
        L3M1[Multi-Syllable Words]
        L3M2[Reading Fluency]
        L3M3[Spelling Patterns]
        L3M4[Paragraph Reading]
    end

    subgraph L4["Level 4 - Advancing"]
        L4M1[Complex Phonics]
        L4M2[Comprehension Skills]
        L4M3[Writing Support]
        L4M4[Vocabulary Building]
    end

    subgraph L5["Level 5 - Mastery"]
        L5M1[Independent Reading]
        L5M2[Advanced Comprehension]
        L5M3[Creative Writing]
        L5M4[Self-Monitoring Skills]
    end

    L1 --> L2 --> L3 --> L4 --> L5
```

## Database Schema Overview

```mermaid
erDiagram
    USERS ||--o{ CHILDREN : has
    CHILDREN ||--o{ ASSESSMENTS : takes
    CHILDREN ||--o{ PROGRESS : tracks
    CHILDREN ||--|| CURRENT_LEVEL : "assigned to"
    LEVELS ||--o{ MODULES : contains
    MODULES ||--o{ ACTIVITIES : contains
    PROGRESS ||--o{ MODULE_PROGRESS : details
    ASSESSMENTS ||--|| ASSESSMENT_RESULTS : produces

    USERS {
        uuid id PK
        string email
        string password_hash
        string role "parent|teacher|admin"
        timestamp created_at
    }

    CHILDREN {
        uuid id PK
        uuid parent_id FK
        string name
        int age
        string dyslexia_type
        int current_level
        timestamp created_at
    }

    ASSESSMENTS {
        uuid id PK
        uuid child_id FK
        string type "initial|periodic"
        json responses
        timestamp taken_at
    }

    ASSESSMENT_RESULTS {
        uuid id PK
        uuid assessment_id FK
        int assigned_level
        json scores
        json dyslexia_profile
        float confidence
    }

    LEVELS {
        int id PK
        string name
        string description
        int order
    }

    MODULES {
        uuid id PK
        int level_id FK
        string name
        string type "phonics|reading|spelling|comprehension"
        int order
    }

    ACTIVITIES {
        uuid id PK
        uuid module_id FK
        string type "interactive|quiz|game|audio"
        json content
        int difficulty
    }

    PROGRESS {
        uuid id PK
        uuid child_id FK
        int level_id FK
        float overall_completion
        timestamp started_at
        timestamp last_activity
    }

    MODULE_PROGRESS {
        uuid id PK
        uuid progress_id FK
        uuid module_id FK
        float accuracy
        int attempts
        int time_spent_mins
        string status "not_started|in_progress|mastered"
    }
```

## Deployment Architecture

```mermaid
graph TB
    subgraph Cloud["Cloud Infrastructure (AWS/GCP)"]
        subgraph Frontend["Frontend Hosting"]
            CDN[CloudFront/CDN]
            Static[S3 Static Assets]
        end

        subgraph Compute["Compute Layer"]
            ALB[Load Balancer]
            API1[FastAPI Instance 1]
            API2[FastAPI Instance 2]
            Worker[Background Workers]
        end

        subgraph DataStores["Data Stores"]
            RDS[(PostgreSQL RDS)]
            ElastiCache[(Redis ElastiCache)]
            S3Content[S3 Content Bucket]
        end

        subgraph MLInfra["ML Infrastructure"]
            SageMaker[SageMaker / Model Endpoint]
            OpenAIGW[OpenAI API Gateway]
        end
    end

    User[👤 User] --> CDN
    CDN --> Static
    CDN --> ALB
    ALB --> API1
    ALB --> API2
    API1 & API2 --> RDS
    API1 & API2 --> ElastiCache
    API1 & API2 --> S3Content
    API1 & API2 --> SageMaker
    SageMaker --> OpenAIGW
    Worker --> RDS
    Worker --> SageMaker
```
