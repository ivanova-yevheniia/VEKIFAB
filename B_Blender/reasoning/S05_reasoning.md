# S05 — Functional Test Station — Engineering Reasoning

*VEKIFAB — AI Factory Planner · Compact Medical Infusion Pump (MF-IP-100) · world position [16.5, 6.0, 0.0]*

> Each pump is powered up and its flow rate verified; results are logged per serial number.

### 1. Why does this station exist?
It is the end-of-line proof of function: electrical and flow-rate test confirms every pump actually works.

### 2. Why is it located here?
After vision (x=16.5) so only assembled, visually-passed units are tested — no wasted test time on obvious rejects.

### 3. Why were these industrial assets selected?
The profile-frame bench, a test fixture driven by a controller/HMI, a barcode scanner for serial logging, e-stop, stack light, a reject box, conveyors and cabinet.

### 4. Why are the dimensions appropriate?
A standard 2.0 m footprint holds the test fixture and flow rig for a ~45 s test.

### 5. Why is this level of automation used?
Automated test cycle: objective pass/fail with a per-unit test record — essential for a medical device.

### 6. Why are these safety systems present?
Emergency stop, stack light and floor markings; the fixture is enclosed, no fence required.

### 7. Why is the operator interaction designed this way?
Minimal operator; results are logged per serial number and failed units are diverted automatically.

### 8. How does this station connect to the previous and next station?
Input conveyor C04 from S04; output conveyor C05 to S06 Packaging.

### 9. What assumptions were made?
The ~45 s test fits the cycle and per-serial medical traceability is required.

### 10. What future improvements are possible?
Parallel test nests, automated reject handling, calibration monitoring and MES/QMS integration.
