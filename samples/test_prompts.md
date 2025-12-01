# BDM Copilot Test Prompts

Collection of realistic customer scenarios for testing the BDM Copilot application.

---

## Prompt #1: Mid-Market Manufacturing (Typical CDW Client)

**Customer Name:** Precision Components Inc.

**Opportunity Value:** $425,000

**Timeline:** 10 weeks

**Discovery Notes:**

```
Discovery meeting with Tom Bradley, IT Director at Precision Components Inc., a mid-sized precision machining company with 850 employees across 3 facilities in the Midwest.

Tom reached out through our CDW account team because their current infrastructure is literally failing. They manufacture precision aerospace and medical device components, and their IT problems are starting to impact production schedules.

Business Critical Issues:
- Main production server crashed twice last month - halted manufacturing for 6 hours each time, cost them $180K in lost production
- ERP system (Epicor) is painfully slow - production managers can't get real-time inventory data, causing material shortages
- Quality inspection photos and CAD drawings filling up storage - currently at 91% capacity on old SAN
- Customer portal for order tracking went down during a major audit - almost lost their largest aerospace customer
- No ability to support remote workers - engineers need to VPN in but performance is terrible
- Ransomware attack at a competitor has the CFO terrified - they have basically no backup or recovery plan

Current Mess:
- Frankenstein environment: 4 Dell PowerEdge R620s (2014 vintage!), 2 HP servers, 1 Cisco UCS (no support contracts on any of it)
- Ancient Dell Compellent SAN with 18TB usable - vendor says parts aren't available anymore
- Running VMware Essentials Plus on the Dell servers - about 45 VMs total
- Backup2Go tape autoloader in the server closet - hasn't been tested in 2+ years
- Veeam Community Edition backing up "some" VMs to the tape and to USB drives Tom takes home (!!)
- Single site - everything in their main facility in Ohio

What Tom Needs:
- Consolidate onto reliable, supported infrastructure - tired of wondering when next failure will happen
- Support 60-75 VMs with room for growth (adding shop floor IoT sensors, MES system planned for next year)
- 40-50TB storage immediately, need to scale to 100TB over next 3 years
- Proper backup solution - CFO wants "ransomware-proof" backups after seeing what happened to their competitor
- Better performance for Epicor ERP and SQL databases
- Simple management - Tom has 2 people on his team, can't handle complexity
- Everything under Dell ProSupport - wants single vendor support experience through CDW

Budget & Business Context:
- CFO approved $400-450K capex budget (this is a big deal for them - family-owned company, very conservative with spending)
- AS9100 certified (aerospace quality standard) - need to demonstrate data integrity and availability for audits
- ISO 13485 coming next year for medical device work - will have stricter IT requirements
- Production runs 24/5 - need high availability but not true 24/7
- Planning to add 4th facility in 18 months - need infrastructure that can extend there

Tom specifically mentioned:
- "We're a Dell shop and want to stay that way - standardization makes my life easier"
- "I need this to just work - I don't have time to become a storage expert"
- "CDW has been great for our endpoints and networking - want them to handle this too"
- "Can we do everything in one purchase order? Finance prefers dealing with one vendor"
- Asked about as-a-service options but CFO is old-school and prefers to own equipment

Perfect CDW opportunity - mid-market client, existing Dell relationship, single PO preference, needs professional services for deployment.
```

---

## Prompt #2: Healthcare System

**Customer Name:** Midwest Regional Hospital

**Opportunity Value:** $950,000

**Timeline:** 14 weeks

**Discovery Notes:**

```
Meeting with Sarah Chen, IT Director at Midwest Regional Hospital, a 450-bed hospital system with 3 locations.

They're struggling with aging infrastructure that can't support modern healthcare demands - PACS imaging systems, EHR (Epic), and telemedicine platforms are all suffering performance issues.

Critical Pain Points:
- PACS (medical imaging) storage running out of space - radiologists complaining about slow image retrieval
- Epic EHR database performance degrading - clinicians experiencing 5-10 second delays during patient care
- No disaster recovery plan - single datacenter, if it goes down patient care is at risk
- Recent ransomware scare at another hospital in their network has board demanding better security
- Compliance audit found gaps in HIPAA technical safeguards for data protection

Current Environment:
- Mix of Dell PowerEdge R740s and older R630s running VMware
- Aging Dell EMC Unity storage at 85% capacity
- 200+ VMs supporting clinical and business applications
- Veeam backing up to aging disk arrays - no immutable backups, no air-gap
- Single site with no DR capability

Technical Requirements:
- 150TB+ storage for PACS archives (7-year retention required by law)
- High-performance storage for Epic database (needs low latency, high IOPS)
- Immutable backups to protect against ransomware
- HIPAA-compliant infrastructure with encryption and audit logging
- 99.99% uptime for clinical systems - downtime literally risks patient lives
- Ability to replicate to DR site 30 miles away

Business Drivers:
- Board approved major IT investment after ransomware incidents at peer hospitals
- Expanding telehealth services - need infrastructure to support video consultations
- New cardiology wing opening in 6 months - will add significant imaging workload
- Meaningful Use and MACRA compliance requirements from CMS

Sarah mentioned they're an existing Dell customer and want to stay with Dell for consistency. She's interested in solutions that can grow with them as they expand services.
```

---

## Prompt #3: Financial Services

**Customer Name:** Global Trade Bank

**Opportunity Value:** $1,100,000

**Timeline:** 12 weeks

**Discovery Notes:**

```
Strategic planning session with Michael Rodriguez, VP of Infrastructure at Global Trade Bank, a regional bank with $8B in assets.

They're modernizing their trading platform infrastructure and need to meet strict regulatory requirements while supporting real-time transaction processing.

Critical Challenges:
- Legacy trading platforms can't handle market volatility - experiencing latency during high-volume trading periods
- Regulatory compliance pressure - SOX, PCI-DSS, and new banking regulations requiring air-gapped backups
- Current storage infrastructure can't deliver the IOPS needed for SQL Server transaction databases
- No immutable backup capability - examiners flagged this in last audit
- Planning M&A activity - need infrastructure that can absorb acquired banks' systems

Current State:
- Dell PowerEdge servers running critical banking applications
- Mix of storage vendors creating management complexity
- 300+ VMs across trading, core banking, and customer-facing applications
- Backups to disk and tape, but no cyber recovery vault
- Primary datacenter in NYC, warm DR site in New Jersey

Requirements:
- Ultra-low latency storage for trading platforms (sub-millisecond response times)
- 200TB+ storage with ability to scale to 500TB as they acquire other banks
- Immutable, air-gapped backups in cyber vault (regulatory requirement)
- Active-active configuration between NYC and NJ datacenters
- PCI-DSS compliant infrastructure for payment card processing
- 99.999% availability for customer-facing banking applications

Business Context:
- Board approved $15M digital transformation budget (this is phase 1)
- Acquiring 2 smaller community banks in next 18 months
- Launching new mobile banking platform requiring high-performance APIs
- Recent ransomware attack at another regional bank has CISO demanding better protection
- Federal regulators increasing scrutiny of operational resilience

Michael emphasized they're committed to Dell infrastructure and need a partner who understands financial services compliance. They're interested in APEX models for OpEx treatment of infrastructure costs.
```

---

## Prompt #4: Retail/E-commerce

**Customer Name:** ShopNow Retail Group

**Opportunity Value:** $850,000

**Timeline:** 12 weeks

**Discovery Notes:**

```
Discovery call with Marcus Thompson, CTO of ShopNow Retail Group, and Lisa Chen, Head of E-commerce Operations.

ShopNow operates 200+ retail stores across North America plus a rapidly growing e-commerce platform. They're facing serious infrastructure challenges as online sales have tripled in the past 2 years.

Critical Pain Points:
- E-commerce platform crashes during peak shopping periods (Black Friday, holiday season)
- Website performance is terrible - pages taking 8-10 seconds to load, customers abandoning carts
- Current infrastructure can't handle the product catalog growth - now at 2 million SKUs with high-res images and videos
- Point-of-sale systems in stores losing connection to central database, causing checkout delays
- No real disaster recovery - they're terrified of what happens if primary datacenter goes down
- Security concerns after a competitor got hit with ransomware last month

Current Environment:
- Aging VMware infrastructure on 6-year-old servers (mix of vendors, mostly Dell PowerEdge R630s)
- SAN storage at 88% capacity with only 65TB usable
- E-commerce database (PostgreSQL) and application servers struggling under load
- Content delivery for product images and videos completely in-house (no CDN)
- Backup is tape-based (!) - takes 36 hours to restore, never tested full recovery
- Separate infrastructure silos for stores vs. e-commerce vs. corporate - no integration

Technical Requirements:
- Need to support 50,000+ concurrent web users during peak (currently max is 12,000)
- Database IOPS requirements are through the roof - current storage can't keep up
- 500TB+ storage for growing product media library (4K images, product videos)
- Must have active-active setup across two datacenters for zero downtime
- Sub-2-second page load times for customer experience
- PCI-DSS compliance for payment card data
- Real-time inventory sync between stores and online (currently 15-minute delay)

Business Context:
- Planning major expansion - acquiring smaller retail chain next quarter (adding 50 stores)
- Board pushing for 60% of revenue from online by 2027 (currently 35%)
- Lost $2.3M in sales last Black Friday due to website crashes
- CMO is demanding better customer experience - site speed is #1 priority
- IT team stretched thin (8 people supporting everything) - need simplified management

Marcus mentioned they're already a Dell shop and want to standardize. Lisa specifically asked about cloud-like flexibility but keeping data on-prem due to data sovereignty concerns for Canadian operations.

Budget is approved, executives want this fixed before next holiday season. They're willing to invest in the right solution.
```

---

## Prompt #5: Higher Education

**Customer Name:** State University System

**Opportunity Value:** $1,200,000

**Timeline:** 16 weeks

**Discovery Notes:**

```
Joint discovery session with Dr. Robert Martinez, VP of IT Services, and Professor Amy Liu, Director of Research Computing at State University System.

They oversee IT infrastructure for a major public university with 45,000 students, 3,500 faculty, and multiple research labs. Currently facing a perfect storm of challenges as they modernize for hybrid learning and research demands.

Critical Challenges:
- Learning management system (Canvas LMS) crashes during peak enrollment periods - 45,000 students trying to register simultaneously
- Research computing clusters are ancient - physicists and bio-informaticians complaining data analysis jobs take weeks instead of hours
- No capacity for AI/ML workloads - losing faculty to other universities with better research infrastructure
- Student housing and campus services running on 8-year-old virtualization infrastructure
- Zero disaster recovery capability - single campus datacenter with no backup site
- Cybersecurity nightmares - they've had 3 ransomware attempts in past year, one nearly succeeded

Current Environment:
- VMware environment on aging Dell PowerEdge R730s (purchased 2016, out of warranty)
- Mix of direct-attached storage and old EqualLogic SAN (EOL, no support)
- Research data scattered across faculty desktop machines and department NAS devices - total chaos
- 850 VMs supporting everything from student email to research databases
- Backup is inconsistent - some systems backed up, many aren't
- No centralized storage - each department bought their own solutions

Technical Requirements Dr. Martinez outlined:
- Need 1,000+ VM capacity for growth (adding online graduate programs, expecting 30% enrollment increase)
- Research computing needs 2 petabytes of fast storage for genomics, climate modeling, particle physics datasets
- Must support GPU workloads for AI/ML research (computer science dept launching new AI program)
- High-performance computing cluster for scientific simulations
- 99.95% uptime for student-facing systems (registration, LMS, email, housing portal)
- Immutable backups to survive ransomware (CIO mandate after recent close call)
- Multi-site capability - want DR site at sister campus 50 miles away

Compliance & Governance:
- FERPA compliance for student educational records (federal requirement)
- NIH and NSF grant requirements for research data management
- Export control regulations for some defense-related research projects
- State audit requirements for financial systems

Business Context:
- Board of Regents approved $15M technology refresh budget (this is phase 1)
- Launching new School of Data Science next fall - needs AI infrastructure ready
- Medical school partnership starting - will need HIPAA-capable infrastructure for patient research data
- Competing with private universities that have better IT - losing faculty and students over poor research computing
- IT team is small for the scale (22 people) - need simplified management

Professor Liu was excited when I mentioned Dell's work with other research universities. She specifically asked about solutions that can handle both traditional VMs and modern containerized workloads for their data science programs.

Dr. Martinez mentioned they're already standardized on Dell servers and want to continue that relationship. He's interested in as-a-service models to smooth out budget cycles.

This is a strategic win - if we do well, we'll get phase 2 (networking refresh) and phase 3 (security infrastructure).
```

---

## Prompt #6: Manufacturing/Industrial

**Customer Name:** TechForge Manufacturing Inc.

**Opportunity Value:** $680,000

**Timeline:** 8 weeks

**Discovery Notes:**

```
Meeting with Jennifer Park, VP of Operations at TechForge Manufacturing.

They're a mid-sized manufacturer with 4 production facilities across the Southeast US. Currently struggling with their aging IT infrastructure that's impacting production efficiency.

Key Pain Points:
- Legacy file servers can't handle CAD/CAM files and IoT sensor data from new smart manufacturing equipment
- No disaster recovery - single site failure would halt all production
- Engineers complaining about slow access to design files (some files 5-10GB)
- Quality control team needs real-time access to production data but current NAS is maxed out
- Compliance requirements for ISO 9001 and automotive industry standards (IATF 16949)

Current Environment:
- Mix of old Dell and HP servers (7+ years old, out of warranty)
- Network-attached storage hitting capacity limits (currently at 92% full with 45TB used)
- No backup solution - just copying files to external drives manually
- VMware environment on aging hardware running production MES and ERP systems
- Remote facilities connecting over VPN with terrible performance

Technical Requirements Jennifer mentioned:
- Need at least 100TB usable storage with room to grow (adding 2 new facilities next year)
- Must support NFS and SMB for mixed Linux/Windows environment
- Need 99.9% uptime SLA - production downtime costs $50K per hour
- Fast file access for engineering team (mentioned something about NVMe?)
- Automated backup and ability to recover from ransomware
- IT team is small (3 people) so needs to be easy to manage

Business Drivers:
- Planning major expansion - 2 new facilities in next 18 months
- Board pushing for digital transformation and Industry 4.0 initiatives
- Recently had a close call with a server failure that almost stopped production
- New contracts require demonstrating robust data protection and compliance

Jennifer seemed very interested when I mentioned Dell's manufacturing customers. She specifically asked about how our solutions handle both structured database data and unstructured CAD files.

Budget approved, need proposal by end of month for Q1 deployment.
```

---

## How to Use These Prompts

1. **Copy the entire Discovery Notes section** (including the triple backticks)
2. **Paste into the BDM Copilot app** in the Discovery Notes field
3. **Fill in the Customer Name, Opportunity Value, and Timeline** fields
4. **Click "Analyze Discovery Notes"**
5. **Review the generated outputs** in all three tabs

Each prompt is designed to test different:

- Industry verticals (Manufacturing, Healthcare, Finance, Retail, Education)
- Deal sizes ($425K - $1.2M)
- Technical requirements (HCI, Storage, HPC, AI/ML, DR)
- Compliance needs (HIPAA, SOX, PCI-DSS, FERPA, ISO)
- Dell product fit (VxRail, PowerStore, PowerScale, PowerProtect, APEX)
