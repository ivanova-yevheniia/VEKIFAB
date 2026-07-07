# S04 — Vision Inspection Station — Engineering Reasoning

*VEKIFAB — AI Factory Planner · Compact Medical Infusion Pump (MF-IP-100) · world position [13.5, 6.0, 0.0]*

> Cameras check assembly correctness and label quality; failed units are diverted automatically.

### 1. Why does this station exist?
It gates quality: automated optical inspection catches assembly and print/label defects before functional test.

### 2. Why is it located here?
Right after the robot cell (x=13.5) so closed, oriented pumps are inspected before any further processing.

### 3. Why were these industrial assets selected?
The profile-frame bench, a camera/scanner sensor, controlled task lighting, an HMI, e-stop, stack light, conveyors and cabinet.

### 4. Why are the dimensions appropriate?
A taller 2.5 m envelope accommodates the camera and lighting mast over a compact bench.

### 5. Why is this level of automation used?
Automated: machine vision is fast, objective and non-contact, removing manual inspection variance.

### 6. Why are these safety systems present?
Emergency stop, stack light and floor markings; the optics are enclosed and the low-risk station needs no fence.

### 7. Why is the operator interaction designed this way?
Minimal operator involvement — a quality inspector monitors the HMI while reject diversion is automatic.

### 8. How does this station connect to the previous and next station?
Input conveyor C03 from S03; output conveyor C04 to S05 Functional Test.

### 9. What assumptions were made?
Image capture and analysis fit in ~20 s, lighting is controlled and a reject bin is present.

### 10. What future improvements are possible?
Deep-learning defect models, multi-view/3D inspection, inline OCR traceability and SPC dashboards.
