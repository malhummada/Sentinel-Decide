🛡 Sentinel-Decide
Human-guided decision engine for Suricata alerts

============================================================

🔍 Sentinel-Decide is a human-guided decision engine designed to help security operators make sense of Suricata alerts without resorting to blind automation.

It reads Suricata eve.json logs, groups alerts into higher-level incidents, proposes defensive actions, and optionally assists in generating nftables rules.
⚠ Nothing is enforced automatically. The human always decides.



🔁 Workflow philosophy:

👁 Observe
🧠 Analyze
📊 Propose
👤 Human decides



❓ WHY THIS PROJECT EXISTS
🚨 Intrusion Detection Systems generate large volumes of alerts.
⚠ Fully automatic responses are risky, while manual inspection does not scale.

Sentinel-Decide sits between detection and enforcement and provides a clear, explainable decision layer without taking control away from the operator.



⚙ WHAT SENTINEL-DECIDE DOES
✔ Reads Suricata eve.json logs
✔ Filters non-actionable informational alerts
✔ Groups alerts into meaningful incidents
✔ Proposes actions such as observe, rate_limit, or block
✔ Aggregates decisions to avoid rule explosion
✔ Generates readable nftables rules files
✔ Asks for explicit user confirmation before any enforcement



🚫 WHAT SENTINEL-DECIDE DOES NOT DO

✖ No automatic blocking
✖ No background daemon or service
✖ No modification of Suricata configuration
✖ No machine learning or AI claims
✖ No firewall policy changes without user approval



🧩 REQUIREMENTS

🖥 Python 3.9 or newer
📡 Suricata with eve.json enabled
🔐 nftables (optional, only if rule export or apply is needed)
🐧 Linux system



📁 PROJECT STRUCTURE

Sentinel-Decide/
explainer/
incident_builder.py
decision_engine.py
decision_aggregator.py
nftables_file_exporter.py
tools/
run_pipeline.py
output/
generated files
README



▶ USAGE

⚡ Automatic analysis (last 5 minutes):

python3 -m tools.run_pipeline auto



⏱ Recent activity:

python3 -m tools.run_pipeline last 5m
python3 -m tools.run_pipeline last 2h
python3 -m tools.run_pipeline last 1d



📅 Since a specific date:

python3 -m tools.run_pipeline since 2025-12-20



📆 Between two dates:

python3 -m tools.run_pipeline between 2025-12-20 2025-12-27



🕒 Explicit timestamps:

python3 -m tools.run_pipeline 2025-12-27T02:40:00 2025-12-28T02:45:00




📦 OUTPUT FILES

Generated under the output directory:


📄 incidents.json
Grouped incidents derived from Suricata alerts


📄 decisions.json
Proposed decision per incident


📄 decision_summary.json
Aggregated decisions per source


📄 cyphorn-guard.nft
nftables rules generated for review



🔐 NFTABLES SAFETY MODEL

🛑 Sentinel-Decide never applies rules automatically.

When nftables rules are generated, the user is prompted to choose:

1️⃣ Do nothing
2️⃣ Copy rules to /etc/nftables.d
3️⃣ Copy and apply rules now

✔ Rules are validated before application
✔ No table flushing
✔ No policy replacement
✔ No hidden changes


🧠 DESIGN PHILOSOPHY

Sentinel-Decide is intentionally simple, deterministic, and explainable.

It does not aim to replace IDS, IPS, or SIEM platforms.
🎯 Its purpose is to assist humans in making informed security decisions while remaining fully in control.


👥 INTENDED AUDIENCE

👨‍💻 Network security engineers
🧑‍✈ SOC analysts
🔥 Firewall administrators
🧠 Operators who distrust blind automation


📌 STATUS

✔ Stable
✔ Intentionally limited
✔ Human-centric

Future improvements will focus on clarity and reliability rather than feature expansion.



⚠ DISCLAIMER ⚠

This software is provided "as is", without any warranty of any kind.
The authors and contributors assume no responsibility for any damage, data loss,
service disruption, or security impact resulting from the use or misuse of this tool.

Sentinel-Decide does not enforce actions automatically.
Any decision to apply firewall rules or security controls remains the sole
responsibility of the user or operator.

Use this tool at your own risk.

============================================================





🛡 Sentinel-Decide (العربية)

============================================================

🔍 Sentinel-Decide هو محرك اقتراح قرارات موجّه للإنسان لمساعدة محللي الأمن في فهم تنبيهات Suricata دون تنفيذ تلقائي.

يقوم بقراءة ملف eve.json، وتجميع التنبيهات في حوادث منطقية، واقتراح إجراءات دفاعية قابلة للمراجعة، مع إبقاء القرار النهائي دائمًا بيد المستخدم.

❓ فكرة المشروع

🚨 أنظمة كشف التسلل تولد عددًا كبيرًا من التنبيهات.
⚠ الأتمتة الكاملة قد تكون خطيرة، بينما التحليل اليدوي وحده لا يكفي.

Sentinel-Decide يعمل كطبقة قرار بين الاكتشاف والتنفيذ دون السيطرة على النظام.

⚙ ماذا يفعل Sentinel-Decide

✔ قراءة تنبيهات Suricata من eve.json
✔ استبعاد التنبيهات غير المهمة
✔ تجميع التنبيهات في حوادث
✔ اقتراح قرارات مثل المراقبة أو تحديد المعدل أو الحظر المؤقت
✔ دمج القرارات لتقليل عدد القواعد
✔ إنشاء قواعد nftables قابلة للمراجعة
✔ طلب موافقة المستخدم قبل أي تنفيذ



🚫 ماذا لا يفعل Sentinel-Decide

✖ لا يمنع تلقائيًا
✖ لا يعمل كخدمة دائمة
✖ لا يغير إعدادات Suricata
✖ لا يستخدم ذكاء اصطناعي
✖ لا يطبق سياسات بدون موافقة



🧠 فلسفة التصميم

🎯 المشروع مبني على الوضوح والتحكم الكامل للمستخدم.
الهدف ليس المنع التلقائي بل دعم القرار البشري بطريقة منظمة وآمنة.



📌 الحالة

✔ مكتمل وظيفيًا
✔ محدود عن قصد
✔ مناسب للنشر والاستخدام الواقعي



⚠ إخلاء المسؤولية ⚠  

يتم توفير هذا البرنامج "كما هو" دون أي ضمان من أي نوع.
لا يتحمل المؤلف أو المساهمون أي مسؤولية عن أي ضرر، فقدان بيانات،
توقف خدمات، أو تأثيرات أمنية ناتجة عن استخدام هذه الأداة أو سوء استخدامها.

مشروع Sentinel-Decide لا ينفذ أي إجراء تلقائيًا.
جميع القرارات المتعلقة بتطبيق قواعد الجدار الناري أو التحكم الأمني
تقع على عاتق المستخدم أو المشغّل فقط.

استخدامك لهذه الأداة يكون على مسؤوليتك الخاصة.


============================================================

