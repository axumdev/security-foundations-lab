from course import p,ul,code,note,refs,step

def extra_pages():
    body='<div class="eyebrow">Read before Week 01</div><h1>Lab operating handbook</h1>'
    body+=p('You are building a small environment in stages. Keep this page open beside the weekly instructions. Do not start all VMs simply because they exist. The host is your physical computer; every other named machine is a guest.')
    body+='<h2>What this course assumes</h2>'+ul('Windows 11 Pro, full local administrator access, and permission to change virtualization settings. Week 1 verifies these assumptions; stop host setup if they are false.','16 GB RAM, an SSD with at least 250 GB free for the initial plan, and functioning cooling. Available disk and memory—not the listing alone—decide what can run.','English reading, good internet for downloads, 6 hours minimum weekly, with extra hours for practice. No previous Linux, Windows administration, or cloud experience is assumed.','Use an authorized Azure sandbox, a dedicated personal learning subscription, or the local alternative in Week 23. No paid training subscription is required.','Plan time for a self-review or an optional mentor review.')
    body+='<h2 id="solo">Learning solo?</h2>'+p('When a lesson calls for mentor review, use these checks yourself. Record a short teach-back or write your explanation from memory.')+ul('Predict what should happen before running the test.','Save the observed result, including a denied case when the lab calls for it.','Explain any mismatch and repeat the test after your fix.','Record how to undo the change and whether the lab is safe to leave running.','Write your case conclusions before opening mentor-answer-key.json. Teachers can hand out the evidence files separately without the key.')
    body+='<h2>Six phases, one foundation</h2><div class="tablewrap"><table><tr><th>Weeks</th><th>Build and understand</th><th>Evidence</th></tr><tr><td>1–6</td><td>Host, Linux, private networking, permissions, services, SSH, firewall</td><td>Independent foundation exam</td></tr><tr><td>7–10</td><td>Windows, domain identity, Group Policy, HTTP/TLS</td><td>Access-control and certificate tests</td></tr><tr><td>11–16</td><td>Wazuh, FIM, Windows telemetry, custom rules, Suricata integration</td><td>Source-to-alert cases</td></tr><tr><td>17–22</td><td>Exposure, response, recovery, containers, small scripts</td><td>Local capstone and risk register</td></tr><tr><td>23–25</td><td>Cloud scope, network, identity, storage, audit and cleanup</td><td>Allowed/denied tests and cost review</td></tr><tr><td>26</td><td>Demonstration and teach-back</td><td>Reviewed portfolio and development plan</td></tr></table></div>'
    body+='<h2>VM inventory and addresses</h2><div class="tablewrap"><table><tr><th>VM</th><th>Private IPv4</th><th>RAM / vCPU</th><th>Disk limit</th><th>Introduced</th></tr><tr><td>UBU01</td><td>10.77.0.11/24</td><td>2 GB / 2</td><td>40 GB</td><td>Week 2 · Linux service/agent/sensor</td></tr><tr><td>UBU02</td><td>10.77.0.12/24</td><td>2 GB / 2</td><td>40 GB</td><td>Week 3 · Linux client</td></tr><tr><td>WIN01</td><td>10.77.0.21/24</td><td>4 GB / 2</td><td>60 GB</td><td>Week 7 · Windows member server</td></tr><tr><td>DC01</td><td>10.77.0.10/24</td><td>4 GB / 2</td><td>60 GB</td><td>Week 8 · domain controller/DNS</td></tr><tr><td>WAZUH01</td><td>10.77.0.30/24</td><td>8 GB / 4</td><td>80 GB</td><td>Week 11 · manager/indexer/dashboard</td></tr></table></div>'
    body+=p('These are training allocations, not production sizing. VHDX maximums total 280 GB before checkpoints, ISOs, exports, logs, and host files. Disks expand as data is written. Reserve additional free space; do not let the SSD fill. Keep about 20% free as an operating target, and pause large installs/exports if available space is tight.')
    body+='<h2>Power profiles for 16 GB</h2>'+ul('<strong>Linux:</strong> UBU01 + UBU02 = 4 GB guest RAM.','<strong>Identity:</strong> DC01 + WIN01 = 8 GB. Linux and Wazuh off.','<strong>Monitoring:</strong> WAZUH01 + UBU01 = 10 GB. All others off.','<strong>Windows capture:</strong> WIN01 alone or with DC01, then shut them down before Wazuh analysis.','<strong>Cloud:</strong> host browser only. Local VMs off.')
    body+=note('Measure actual host memory in Task Manager. Fixed guest memory plus host/browser use can still cause paging on 16 GB. If the monitoring profile is unstable, stop and arrange more RAM or a mentor-provided server; do not lower Wazuh below the documented allocation and call it equivalent. A 32 GB upgrade would be helpful but is not assumed. Verify compatible modules in your computer manufacturer’s documentation before purchasing.')
    body+='<h2>Network modes</h2><div class="tablewrap"><table><tr><th>Mode</th><th>Connections</th><th>Permitted work</th></tr><tr><td>Private exercise</td><td>One adapter per guest → CyberLab-Private; static IP; no gateway</td><td>Tests, scans of named guests, dummy exposure, response exercises</td></tr><tr><td>Update</td><td>One adapter → Default Switch; DHCP</td><td>Download/patch only. Stop test services first. Return private before tests.</td></tr><tr><td>Temporary management</td><td>UBU01 keeps private adapter and temporarily adds Default Switch for a host SSH tunnel</td><td>Dashboard/file transfer only. No scans or exposed training container. Remove afterward.</td></tr></table></div>'
    body+=p('The private segment has no host network interface, DHCP, gateway, or internet route. Domain clients use DC01 for internal DNS only. The Default Switch provides managed connectivity; its subnet and addresses may change. Never hardcode a Default Switch IP from another session. A dual-homed UBU01 is a boundary exception even without routing; minimize its duration.')
    body+=code('Windows HOST 16 GB\n  Hyper-V\n    CyberLab-Private 10.77.0.0/24 — no gateway\n      DC01 .10       UBU01 .11       UBU02 .12\n      WIN01 .21      WAZUH01 .30\n\nNormal: host reaches guests through Hyper-V console only.\nTemporary dashboard path:\n  host localhost:8443 -> SSH to UBU01 Default-Switch IP\n                     -> WAZUH01 .30:443 via private NIC\n  No bridge / no IP forwarding; remove extra NIC afterward.','Topology • logical inventory, not simultaneous power-on')
    body+='<h2>Every session: start, test, close</h2>'+ul('Read the week’s prerequisites and power-on plan. Record date/time, VM names, and the one objective for the session.','Check host free memory/disk. Start only the required guests. Verify hostname and IP before copying commands.','Before a change, save the specific configuration file and note how to undo it. Use a named checkpoint only where appropriate.','State the expected result, run one step, inspect actual output, and save sanitized evidence. Stop if a command fails rather than pasting the rest of a block.','For tests, verify Private switch, one adapter, and no default route. For temporary management, verify no training container or simulator is running.','At the end, stop foreground tools/containers, remove temporary rules/adapters, record unfinished work, and shut guests down through their OS. Close cloud resources as instructed.')
    body+='<h2>Command and editor survival guide</h2>'+ul('Each dark command block names its execution location. HOST means your physical computer; UBU01 and other names mean that guest. PowerShell and Bash syntax are not interchangeable.','REPLACE_ tokens are instructions to substitute an actual observed value. Never paste them unchanged. Angle-bracket placeholders in vendor documentation work similarly.','In nano: Ctrl+O → Enter saves; Ctrl+X exits; Ctrl+W searches. Use spaces in YAML. XML opening/closing tags must match.','Ctrl+C stops a foreground command. q exits less, man, and many pagers. Do not close the whole VM merely to leave a terminal tool.','Linux paths are case-sensitive. ~/ means the current user’s home. 127.0.0.1 means this machine, so it refers to different machines in host and guest terminals.','sudo elevates one Linux command. Windows administrator PowerShell is opened using Run as administrator. Never make a habit of pasting unreviewed internet scripts.')
    body+='<h2>Reusable Linux network procedure</h2>'+p('After Week 3, UBU01/02 have /etc/netplan/01-lab.yaml. For update mode, shut down, move the sole adapter to Default Switch, boot using the console, edit that file to the DHCP example below, validate, and apply. Keep a copy of your static file in the home directory. Do not leave old active YAML files that conflict.')
    body+=code('network:\n  version: 2\n  ethernets:\n    eth0:\n      dhcp4: true\n      dhcp6: false\n      accept-ra: false','Guest netplan • update mode; replace eth0 with observed interface')
    body+=code('sudo netplan generate\nsudo netplan try\nip -br address\nip route\nresolvectl status\ngetent hosts ubuntu.com','Guest • verify DHCP/update mode')
    body+=p('To return private, shut down, reconnect CyberLab-Private, restore the static YAML for that VM’s address, run the same validation, and confirm no default route. The Ubuntu DNS search commands may fail in private mode by design. Use IPs for Linux peer tests.')
    body+='<h2>Temporary management: exact extra steps</h2>'+p('Week 11 introduces the tunnel. Shut UBU01 down, add exactly one Default Switch adapter, boot, and identify the new interface by its MAC address; do not assume it is eth1. In the existing netplan ethernets mapping add that new interface using dhcp4: true, dhcp6: false, accept-ra: false. Preserve eth0’s 10.77.0.11 address. If it is eth1, the temporary combined file looks like this:')
    body+=code('network:\n  version: 2\n  ethernets:\n    eth0:\n      dhcp4: false\n      dhcp6: false\n      accept-ra: false\n      addresses: [10.77.0.11/24]\n    eth1:\n      dhcp4: true\n      dhcp6: false\n      accept-ra: false','UBU01 • temporary combined netplan')
    body+=p('Apply with netplan try. On the host, ipconfig shows the host’s vEthernet (Default Switch) IPv4. In UBU01 run the following with that IP and observed new interface:')
    body+=code('sudo ufw allow in on eth1 from REPLACE_HOST_DEFAULT_IP to any port 22 proto tcp\nsysctl net.ipv4.ip_forward\nsysctl net.ipv6.conf.all.forwarding','UBU01 • temporary management rule')
    body+=p('Both forwarding values should be 0; if Docker left IPv4 forwarding enabled, ensure all containers are stopped, then set sudo sysctl -w net.ipv4.ip_forward=0 for this management session. Do not configure a bridge. Copy a new host public key through the console only if needed: on the host run ssh-keygen -t ed25519 -f "$env:USERPROFILE\\.ssh\\cyberlab_host" and inspect its .pub file. In UBU01 use mkdir -p ~/.ssh, nano ~/.ssh/authorized_keys, append the single public-key line, then chmod 700 ~/.ssh and chmod 600 ~/.ssh/authorized_keys. Keep all existing keys.')
    body+=code('ssh -i "$env:USERPROFILE\\.ssh\\cyberlab_host" -N -L 8443:10.77.0.30:443 learner@REPLACE_UBU01_DEFAULT_IP','HOST • PowerShell')
    body+=p('Open https://localhost:8443 while the tunnel runs. Before accepting the certificate exception, inspect WAZUH01’s configured dashboard certificate path in /etc/wazuh-dashboard/opensearch_dashboards.yml and run sudo openssl x509 -in ACTUAL_CERT_PATH -noout -fingerprint -sha256 in its console. Compare to the browser certificate’s SHA-256 fingerprint. This is a lab-only exception, not blanket trust for other sites.')
    body+=p('For file transfers from the host use scp -i with the same key. Close the tunnel, shut UBU01 down, remove the added Default Switch adapter in Hyper-V, boot using the console, remove its YAML entry, reapply netplan, and delete the temporary ufw rule by its current number. Confirm no default route. After Week 20, Docker may need a service restart before a later container-network exercise; only do that in private mode.')
    body+='<h2>Backup and checkpoint rules</h2>'+ul('A checkpoint is short-term rollback inside a VM disk chain. It is not a backup, and reverting may lose collected evidence or enrolled-agent state.','Keep a clean baseline and at most a few recent change checkpoints. Delete through Hyper-V Manager and wait for merging; never manually delete AVHDX files.','Before AD exercises, prefer an orderly shutdown and coordinated export of both domain machines. Do not randomly revert one domain member or controller to repair an identity problem.','Course evidence belongs outside guest disks too. Keep private originals separate from sanitized portfolio copies. Off-device backups need separate storage that the laptop does not supply by itself.')
    body+='<h2>Version policy and downloads</h2>'+p('Baseline: Windows 11 Pro host, Ubuntu Server 24.04 LTS guests, Windows Server 2025 Evaluation Desktop Experience, Wazuh 4.14 family (4.14.7 packages observed during authoring), OISF stable Suricata (8.x documentation), Ubuntu-packaged Lynis/restic/Docker, official nginx image. Exact patch versions can change. Save the real installed versions and consult linked official documentation before each installation. Do not assume a newer major release is interchangeable.')
    body+=p('Stage downloads just before the relevant week rather than filling the SSD on day one. Budget roughly several GB per OS ISO, additional packages/images, and repeated security updates; actual downloads vary. Retain verified installers where space permits. Windows evaluations have time limits and activation requirements: install in Week 7/8, record expiration, and never work around licensing by changing the clock. All security stacks here are open-source tools except explicitly named Windows/Sysmon/Azure components; free evaluation is not open-source licensing.')
    body+='<h2>When to stop and ask the mentor</h2>'+ul('The target might be the real host, another person’s system, or a cloud group outside scope.','The expected isolated network has an unexplained route or adapter.','A command asks to delete, format, or overwrite data you have not identified.','A tool needs more resources than this laptop can provide.','The actual software release or schema differs enough that tests fail. Preserve the error and version; do not improvise a chain of unverified fixes.')
    body+=refs(('Wazuh capacity guidance','https://documentation.wazuh.com/current/quickstart.html'),('Hyper-V networking','https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/plan/plan-hyper-v-networking-in-windows-server'))
    pages=[('lab-handbook','Lab handbook',body)]

    body='<div class="eyebrow">Instructor edition</div><h1>Mentor guide</h1>'+p('Your role is to make the learner explain and verify systems rather than merely complete installations. His development experience helps with structured thinking; the course deliberately limits coding to useful administrative automation. Use the labs to discover which kind of security work he enjoys.')
    body+='<h2>Weekly review · 30–45 minutes</h2>'+ul('5 minutes: learner states the system and intended behavior without reading the guide.','10 minutes: learner shows one positive and one negative test, with fresh output where feasible.','10 minutes: ask why the control works and where it fails.','5–10 minutes: introduce one reversible fault or ask for a diagnosis of an existing failure.','5 minutes: record score, one improvement, and the next prerequisite. Keep the review within the six-hour core budget.')
    body+='<h2>One rubric throughout the course</h2><table><tr><th>Dimension</th><th>0</th><th>1</th><th>2</th></tr><tr><td>Build</td><td>Not working</td><td>Works with substantial help</td><td>Works and can be reproduced</td></tr><tr><td>Explain</td><td>Cannot explain key behavior</td><td>Partial explanation</td><td>Correct layer-by-layer explanation</td></tr><tr><td>Verify</td><td>No credible tests</td><td>Only happy path</td><td>Positive and negative tests</td></tr><tr><td>Troubleshoot</td><td>Random changes</td><td>Needs guided hypotheses</td><td>Evidence → hypothesis → narrow repair</td></tr><tr><td>Document</td><td>Missing or misleading</td><td>Partial outputs</td><td>Reproducible evidence, limits, rollback</td></tr></table>'
    body+=p('Weekly pass target: 7/10 with no zero in Verify. Milestone/final pass: 8/10 plus required demonstrations. Boundary mistakes or exposed secrets require correction regardless of score. Grade the learner’s reasoning, not laptop speed or whether a vendor installer encountered a transient failure. A transparent failed test can earn credit for troubleshooting but does not pass an unfulfilled build requirement.')
    body+='<h2>Milestone gates</h2><table><tr><th>Week</th><th>Required demonstration</th><th>Before advancing</th></tr><tr><td>6</td><td>Networking, file access, service diagnosis, SSH key-only access</td><td>Correctly identifies host/guest and isolation</td></tr><tr><td>10</td><td>Domain DNS, policy application, trusted TLS test</td><td>Explains identity versus connectivity</td></tr><tr><td>16</td><td>FIM and Suricata source-to-alert chains</td><td>Positive/negative rule tests and visibility limits</td></tr><tr><td>22</td><td>Integrated local capstone and restore</td><td>8/10 and current evidence</td></tr><tr><td>25</td><td>Cloud least privilege, network denial, cleanup</td><td>No resources unintentionally left billing</td></tr><tr><td>26</td><td>Portfolio + fresh case + oral review</td><td>8/10 and honest scope/limitations</td></tr></table>'
    body+='<h2>Fault bank · instructor controlled</h2>'+p('Choose exactly one fault, record its prior state, and keep console access. Tell the learner the affected service, not the cause. Never alter the host’s actual networking, account, or data as an exam. Restore the original value after the learner’s attempt if needed.')
    body+='<table><tr><th>Stage</th><th>Fault</th><th>Expected reasoning and repair</th></tr><tr><td>Week 6</td><td>Stop nginx on UBU01</td><td>Peer reachable → no listener → service stopped → start → remote HTTP works</td></tr><tr><td>Week 6</td><td>Change sample file 640 → 600</td><td>Identity and path traversal → owner/group bits → restore 640 → allowed/denied tests</td></tr><tr><td>Week 9</td><td>Unlink only Lab-Logon-Notice</td><td>Inspect OU/link and gpresult → relink → gpupdate → applied result</td></tr><tr><td>Week 12</td><td>Stop only UBU01 Wazuh agent</td><td>Endpoint service/connection → manager agent status → restart → fresh FIM test</td></tr><tr><td>Week 16</td><td>Typo only in Suricata localfile path</td><td>EVE present → agent path wrong → correct/restart → new event centrally</td></tr><tr><td>Week 22</td><td>Remove one nginx TLS symlink</td><td>HTTP works/HTTPS not listening → enabled sites → restore symlink → nginx -t/reload → TLS trust test</td></tr></table>'
    body+='<h2>Answer anchors</h2><details><summary>Foundations and identity</summary>'+ul('A private switch gives guest-to-guest networking; Default Switch adds connectivity. Failure of a public ping alone is not proof of isolation.','File access depends on identity, permissions, and parent-directory traversal; opening access broadly masks the cause.','DNS is required for domain discovery. Public DNS cannot resolve the private domain’s AD service records.','Group membership affects tokens; re-logon is necessary for clean access-change tests. Policy-editor configuration alone does not prove GPO application.','TLS requires identity/trust validation. A hash verifies bytes, not confidentiality.')+'</details>'
    body+='<details><summary>Detection and response</summary>'+ul('A live source, agent, manager rule, index, and dashboard have distinct failure symptoms. A logtest match is not proof of ingestion.','Sysmon replay proves captured data and parsing; it does not prove continuous native Windows collection.','The Suricata lab sees UBU01 traffic. Neither sharing a switch nor an “active” service establishes full coverage.','An alert needs context and disposition. Training markers/pings are expected and cannot justify an attack claim.','Triage preserves volatile information before containment where feasible. A restore must be validated by content/hash and actual usability.')+'</details>'
    body+='<details><summary>Cloud</summary>'+ul('Resource Contributor and data roles are separate; a learner with inherited data permissions cannot validly perform the Reader-only negative test.','An access-denied result can come from networking, identity, or permissions. Hold other variables constant.','Activity log covers management actions; blob reads require storage data logging.','Budget alerts can lag and are not a hard cap. Deallocated compute can leave disks/IPs/storage charges.','MFA, scoped roles, dummy data, narrow ingress, and verified cleanup are part of the cloud exercise.')+'</details>'
    body+='<h2>Support the six-hour learner</h2>'+p('Use the first hour of a review to repair a blocking prerequisite only when necessary; otherwise keep the review short. Weeks 11, 13, and 24 can be heavier because of installation or access friction. At six hours weekly, remove optional exercises first and use Week 22 for catch-up. If core work still exceeds the budget, extend the calendar; do not omit basic validation to preserve an artificial six-month finish date.')
    body+='<h2>Preparation for the instructor</h2>'+ul('Before Week 1: verify admin access, host backups, recovery key availability, and free resources.','Before Week 7: confirm evaluation downloads are available and the learner can activate them legitimately.','Before Week 11: inspect actual memory use; decide whether the 10 GB profile is practical. Validate the current Wazuh release and agent compatibility.','Before Week 13: verify the replay export/import path; native Windows monitoring is an optional resource upgrade.','Before Week 23: provide a sandbox, learner MFA identity, scoped access, budget, and a cleanup agreement.','Before public reuse: pilot the full course on a fresh machine; record actual timings, tool releases, ambiguous steps, and install failures.')
    body+='<h2>Reuse and future publishing</h2>'+p('The delivery uses static HTML and CSS: no accounts, payments, student database, or backend are required to read it. Host it later under your own domain if desired. Add student accounts or grading only when there is a concrete need. Keep a versioned course source, a changelog, and separate private instructor material if examination secrecy becomes important. In this first family edition, mentor answers are visible in the same bundle.')
    body+=p('Do not label the course open source until you choose a license. For future redistribution, review the licenses of your original content and any bundled third-party material; this edition links to vendor documentation and does not redistribute OS ISOs or vendor logos. No paid-program or certification requirement is assumed. Treat this as edition 1.0 for instructor pilot validation, not a claim that every VM command has been executed on his laptop.')
    pages.append(('mentor','Mentor guide',body))

    body='<div class="eyebrow">Copy into your notebook</div><h1>Evidence templates</h1>'+p('Use plain text, Markdown, or your preferred editor. Store private originals separately. Replace the field labels with your own observations; do not copy an expected result as though you observed it.')
    templates={
    'Weekly lab report':'''Week / title:
Date and UTC time:
Objective in my own words:
VMs powered on and addresses:
OS/tool versions:
Scope and network mode:
Baseline / backup:
Steps taken (command + location + reason):
Expected result:
Actual result:
Positive test:
Negative test:
Failure and diagnosis:
Rollback / cleanup:
Evidence filenames and SHA-256 hashes:
What this proves:
What this does not prove:
Three sentences explaining what I learned:
Mentor score / next action:''',
    'Detection rule card':'''Rule name / ID / revision / owner:
Purpose:
Data source and required collection settings:
Schema and relevant fields:
Logic in plain language:
Positive sample and expected rule ID:
Negative sample and expected result:
Live collection test result:
False positives:
False negatives / visibility gaps:
Response action and escalation:
Replay or live? Original time versus ingestion time:
Version tested / review date:''',
    'Incident report':'''Case ID / status / severity:
Scope and authorized simulation statement:
Summary for a nontechnical reader:
Affected assets and dummy data:
UTC timeline (time | observed fact | source):
Evidence manifest (file | origin | collector | time | hash):
Facts:
Hypotheses:
Unknowns:
Containment and validation:
Cause / remediation:
Recovery and validation:
Business impact:
Limitations:
Lessons and assigned follow-ups:
Closure decision and supporting evidence:''',
    'Change and rollback record':'''Change ID / owner / date:
Purpose and scope:
Current setting:
Proposed setting:
Expected effect:
Risk / access that could be lost:
Backup of the specific config:
Syntax/preflight test:
Implementation:
Allowed behavior test:
Denied behavior test:
Rollback steps:
Rollback result (if exercised):
Final state and evidence:''',
    'Risk and remediation register':'''ID | asset | weakness | evidence | likelihood | impact
Current control:
Residual risk:
Proposed action:
Owner and due date:
Status (unverified / confirmed / remediated / accepted):
Retest and result:
Acceptance reason and review date (if deferred):''',
    'Cloud session worksheet':'''Tenant / subscription (private):
Resource group / region:
Learner identity and role scope:
MFA confirmed:
Approved budget / currency / duration:
Calculator estimate and date:
Alert recipients and thresholds:
Resources expected:
Management and data permissions:
Allowed and denied tests:
Logging enabled and coverage limitations:
Cleanup owner and deadline:
Resources removed / verified at:
Delayed cost review date and result:''',
    'Version manifest':'''Course edition:
Host Windows edition/build:
Ubuntu release / kernel:
Windows guest version / evaluation expiration:
Wazuh manager / indexer / dashboard / agent versions:
Suricata version:
Lynis / restic / Docker versions:
Container image tag and digest:
Installer source URL / filename / download date:
Published checksum / computed checksum / comparison:
Documentation changed from course? What changed:
Mentor review:'''
    }
    for title,t in templates.items():body+='<h2>'+title+'</h2>'+code(t,'Template • copy and fill in')
    body+='<h2>Evidence file naming</h2>'+p('Use names such as week16-LAB016-suricata-alert-2026-10-15T140000Z.json. Keep screenshots tightly cropped around relevant output. Never include passwords, private keys, cloud tokens, personal messages, or unrelated logs. A screenshot is useful context; preserve machine-readable output too when it matters.')
    pages.append(('templates','Evidence templates',body))

    body='<div class="eyebrow">Quick reference</div><h1>Glossary and troubleshooting</h1>'
    glossary={'Agent':'Software on an endpoint that observes or reports information.','Alert':'A signal produced when evidence matches detection logic; it requires interpretation.','Authentication':'Proving an identity.','Authorization':'Deciding which actions an identity may perform.','Baseline':'A recorded starting state used for comparison.','CIDR /24':'IPv4 subnet notation; /24 leaves 8 host bits and corresponds to 255.255.255.0.','Control plane':'Operations that create or configure resources.','Data plane':'Operations that use the data inside resources, such as reading a blob.','DNS':'Name resolution, including records that help clients discover services.','Endpoint':'A machine being used or monitored.','Event':'A recorded occurrence; not every event becomes an alert.','Firewall':'A rule system that permits or blocks traffic at a boundary.','FIM':'File integrity monitoring; detects selected file changes against a baseline.','Gateway':'A router used to reach other networks.','Guest':'A virtual machine’s operating system.','Hash':'A fixed-size digest used to compare data integrity; not encryption.','Host':'The real computer running the hypervisor.','Hypervisor':'Software that runs and manages virtual machines.','IAM':'Identity and access management.','Indexer':'A component that stores data in a searchable form.','IOC':'Indicator of compromise; a clue, not conclusive attribution.','Least privilege':'Only the access required for a task.','NAT':'Address translation; outbound connectivity is not the same as network isolation.','NIC':'Network interface card; virtual guests use virtual interfaces.','NSG':'Azure network security group, a cloud traffic filter.','PCAP':'A packet-capture file.','Port':'A transport-layer service number, such as TCP 443.','Private key':'Secret cryptographic material that must stay protected.','RPO':'Maximum tolerable time window of lost data.','RTO':'Target time to restore service.','SIEM':'Security information and event management: collecting, searching, and analyzing security evidence.','Signature':'A defined pattern used to recognize a type of event or traffic.','Snapshot':'A saved state; its meaning depends on the tool and is not automatically an independent backup.','Subnet':'A range of addresses treated as local on an interface.','TLS':'A protocol that encrypts transport and authenticates peers when correctly validated.','Token':'A representation of authenticated identity and/or access rights; also used for bearer credentials.','UTC':'A standard time reference for comparing events across systems.','VHDX':'Hyper-V virtual-disk file format.','Vulnerability':'A weakness that can be exploited; a scanner suggestion still needs validation.'}
    body+='<table><tr><th>Term</th><th>Meaning</th></tr>'+''.join('<tr><td>'+k+'</td><td>'+v+'</td></tr>' for k,v in glossary.items())+'</table>'
    body+='<h2>Diagnose by layer</h2>'+ul('1. Scope: am I on the correct host/guest? Run hostname/whoami or Windows equivalents.','2. Resources: enough RAM/disk? Inspect Task Manager, free -h, df -h.','3. Link: correct virtual switch and adapter? Check Hyper-V Settings and ip -br link.','4. Address/route: correct unique IP and mask? Check ip -br address, ip route, ipconfig /all.','5. Name: can the correct DNS server resolve the required name? Test an IP separately from a name.','6. Transport: is the service listening on the right address/port? Use ss or Get-NetTCPConnection.','7. Policy: does a firewall or access rule intentionally deny the action? Test from the correct source identity/address.','8. Service: running and valid config? Use systemctl status, nginx -t, sshd -t, or Event Viewer.','9. Data pipeline: source event → collector → manager → index → dashboard. Inspect each boundary.','10. Interpretation: correct timestamp, schema, expected behavior, and scope? An old alert is not evidence of a new test.')
    body+='<h2>Common symptoms</h2><table><tr><th>Symptom</th><th>First checks</th></tr><tr><td>Linux ISO will not boot</td><td>Generation 2 DVD attachment/boot order; Microsoft UEFI Certificate Authority template</td></tr><tr><td>Guest is very slow</td><td>Actual host RAM pressure, other running VMs, disk free space, update load</td></tr><tr><td>apt cannot resolve a name</td><td>Expected in private mode; use controlled DHCP update mode and verify DNS</td></tr><tr><td>Connection refused</td><td>Reached an address but likely no listener or an explicit reject; inspect service/socket</td></tr><tr><td>Connection times out</td><td>Wrong address, route, firewall drop, or unavailable peer; narrow by layer</td></tr><tr><td>Permission denied</td><td>Exact identity, parent directories, ACL/group membership, new session needed?</td></tr><tr><td>Domain join fails</td><td>Domain DNS, DC health, time, credentials, evaluation state</td></tr><tr><td>Wazuh dashboard empty</td><td>Fresh source event, active agent, manager alert file, index health, time range</td></tr><tr><td>Suricata has no alerts</td><td>Actual packet visibility, interface, rule loading, matching test, output path</td></tr><tr><td>Cloud 403</td><td>Correct identity, role scope, network restriction, auth method, propagation</td></tr><tr><td>Restore reports success</td><td>Locate restored file, compare hash/content, measure recovery—not just exit status</td></tr></table>'
    body+=p('After 20–30 minutes without progress, stop changing settings. Save the exact error, last known working state, recent changes, versions, and tests already attempted. Ask the mentor a focused question with that evidence. This is professional escalation, not failure.')
    pages.append(('glossary','Glossary and troubleshooting',body))
    return pages
