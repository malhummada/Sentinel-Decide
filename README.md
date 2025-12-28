<br>
🛡 Sentinel-Decide
Decision engine for Suricata alerts

---

🔍 Sentinel Decide is a a decision engine designed to help security operators make sense of Suricata alerts without resorting to blind automation.

It reads Suricata eve.json logs, groups alerts into higher-level incidents, proposes defensive actions, and optionally assists in generating nftables rules.
⚠ Nothing is enforced automatically.

---
🔁 Workflow philosophy:

👁 Observe 
🧠 Analyze 
📊 Propose 
👤 Administrator decides 

---

❓ WHY THIS PROJECT EXISTS
🚨 Intrusion Detection Systems generate large volumes of alerts.
⚠ Fully automatic responses are risky, while manual inspection does not scale.

Sentinel-Decide sits between detection and enforcement and provides a clear, explainable decision layer without taking control away from the operator.


---
⚙ WHAT SENTINEL-DECIDE DOES

✔ Reads Suricata eve.json logs

✔ Filters non-actionable informational alerts

✔ Groups alerts into meaningful incidents

✔ Proposes actions such as observe, rate_limit, or block

✔ Aggregates decisions to avoid rule explosion

✔ Generates readable nftables rules files

✔ Asks for explicit user confirmation before any enforcement


---
🚫 WHAT SENTINEL-DECIDE DOES NOT DO

✖ No automatic blocking

✖ No background daemon or service

✖ No modification of Suricata configuration

✖ No machine learning or AI claims

✖ No firewall policy changes without user approval



---
🧩 REQUIREMENTS

🖥 Python 3.9 or newer

📡 Suricata with eve.json enabled

🔐 nftables (optional, only if rule export or apply is needed)

🐧 Linux system



---
📁 PROJECT STRUCTURE

Sentinel-Decide/

<br>
explainer/

incident_builder.py

decision_engine.py

decision_aggregator.py

nftables_file_exporter.py

<br>
tools/

run_pipeline.py

<br>
output/

generated files


README


---


▶ USAGE

⚡ Automatic analysis (last 5 minutes):

python3 -m tools.run_pipeline auto

---
⏱ Recent activity:

python3 -m tools.run_pipeline last 5m

python3 -m tools.run_pipeline last 2h

python3 -m tools.run_pipeline last 1d

---
📅 Since a specific date:

python3 -m tools.run_pipeline since 2025-12-20

📆 Between two dates:

python3 -m tools.run_pipeline between 2025-12-20 2025-12-27


---


📦 OUTPUT FILES

Generated under the output directory:


📄 incidents.json
Grouped incidents derived from Suricata alerts


📄 decisions.json
Proposed decision per incident


📄 decision_summary.json
Aggregated decisions per source


📄 sentinel-decide.nft
nftables rules generated for review


---


🔐 NFTABLES SAFETY MODEL

🛑 Sentinel-Decide never applies rules automatically.

When nftables rules are generated, the user is prompted to choose:

1️⃣ Do nothing

2️⃣ Copy rules to /etc/nftables.d

3️⃣ Copy and apply rules now

---

✔ Rules are validated before application

✔ No table flushing

✔ No policy replacement

✔ No hidden changes

---


🧠 DESIGN PHILOSOPHY

Sentinel-Decide is intentionally simple, deterministic, and explainable.

It does not aim to replace IDS, IPS, or SIEM platforms.

🎯 Its purpose is to assist admin in making informed security decisions while remaining fully in control.

---
👥 INTENDED AUDIENCE

👨‍💻 Network security engineers
🧑‍✈ SOC analysts
🔥 Firewall administrators
🧠 Operators who distrust blind automation

---

📌 STATUS

✔ Stable
✔ Intentionally limited
✔ Administrator centric

Future improvements will focus on clarity and reliability rather than feature expansion.


---

⚠ DISCLAIMER ⚠

This software is provided "as is", without any warranty of any kind.
The authors and contributors assume no responsibility for any damage, data loss,
service disruption, or security impact resulting from the use or misuse of this tool.

Sentinel-Decide does not enforce actions automatically.
Any decision to apply firewall rules or security controls remains the sole
responsibility of the user or operator.

Use this tool at your own risk.


<br><br>

---
<div dir="rtl">

  
🛡 Sentinel-Decide (العربية)

---

<div dir="rtl">
  
🔍 Sentinel-Decide 

هو محرك اقتراح قرارات، صُمّم لمساعدة مشغلي الأمن على فهم تنبيهات Suricata دون اللجوء إلى الأتمتة العمياء.

يقوم بقراءة سجلات eve.json الخاصة بـ Suricata، وتجميع التنبيهات في حوادث عالية المستوى، واقتراح إجراءات دفاعية، مع إمكانية المساعدة في إنشاء قواعد nftables.
⚠ لا يتم تنفيذ أي إجراء تلقائيًا.
</div>
------------------------------------------------------------

🔁 فلسفة سير العمل

👁 المراقبة  
🧠 التحليل  
📊 الاقتراح  
👤 قرار بشري  

------------------------------------------------------------

❓ لماذا وُجد هذا المشروع

🚨 أنظمة كشف التسلل تولد كميات كبيرة من التنبيهات.
⚠ الاستجابة التلقائية بالكامل خطيرة، بينما الفحص اليدوي لا يتوسع بشكل كافٍ.

Sentinel-Decide يعمل بين الاكتشاف والتنفيذ، ويقدّم طبقة قرار واضحة وقابلة للتفسير دون سحب التحكم من المشغّل.

------------------------------------------------------------

⚙ ماذا يفعل Sentinel-Decide

✔ قراءة سجلات eve.json الخاصة بـ Suricata  
✔ استبعاد التنبيهات غير القابلة للتنفيذ  
✔ تجميع التنبيهات في حوادث منطقية  
✔ اقتراح إجراءات مثل المراقبة أو تحديد المعدل أو الحظر  
✔ دمج القرارات لتجنب تضخم عدد القواعد  
✔ إنشاء ملفات قواعد nftables قابلة للقراءة  
✔ طلب تأكيد صريح من المستخدم قبل أي تنفيذ  

------------------------------------------------------------

🚫 ماذا لا يفعل Sentinel-Decide

✖ لا يمنع تلقائيًا  
✖ لا يعمل كخدمة أو daemon  
✖ لا يغيّر إعدادات Suricata  
✖ لا يستخدم تعلم آلي أو ذكاء اصطناعي  
✖ لا يطبّق سياسات جدار ناري دون موافقة المستخدم  

------------------------------------------------------------

🧩 المتطلبات

🖥 Python 3.9 أو أحدث  
📡 Suricata مع تفعيل eve.json  
🔐 nftables (اختياري، فقط عند التصدير أو التطبيق)  
🐧 نظام Linux  

------------------------------------------------------------

📁 هيكل المشروع

Sentinel-Decide/
  explainer/
    incident_builder.py
    decision_engine.py
    decision_aggregator.py
    nftables_file_exporter.py
  tools/
    run_pipeline.py
  output/
    ملفات ناتجة
  README

------------------------------------------------------------

▶ طريقة الاستخدام

⚡ تحليل تلقائي (آخر 5 دقائق):

python3 -m tools.run_pipeline auto

⏱ نشاط حديث:

python3 -m tools.run_pipeline last 5m  
python3 -m tools.run_pipeline last 2h  
python3 -m tools.run_pipeline last 1d  

📅 من تاريخ محدد:

python3 -m tools.run_pipeline since 2025-12-20

📆 بين تاريخين:

python3 -m tools.run_pipeline between 2025-12-20 2025-12-27

------------------------------------------------------------

📦 ملفات الإخراج

يتم إنشاء الملفات التالية داخل مجلد output:

📄 incidents.json  
  الحوادث المجمعة من تنبيهات Suricata

📄 decisions.json  
  القرارات المقترحة لكل حادثة

📄 decision_summary.json  
  القرارات المجمعة لكل مصدر

📄 sentinel-decide.nft  
  قواعد nftables الجاهزة للمراجعة

------------------------------------------------------------

🔐 نموذج أمان nftables

🛑 Sentinel-Decide لا يطبّق أي قواعد تلقائيًا.

عند إنشاء قواعد nftables، يُطلب من المستخدم الاختيار بين:

1️⃣ عدم التنفيذ  
2️⃣ نسخ القواعد إلى /etc/nftables.d  
3️⃣ النسخ والتنفيذ فورًا  

✔ يتم التحقق من القواعد قبل التطبيق  
✔ لا يتم مسح الجداول  
✔ لا يتم تغيير السياسات  
✔ لا توجد تغييرات خفية  

------------------------------------------------------------

🧠 فلسفة التصميم

Sentinel-Decide أداة بسيطة، حتمية، وقابلة للتفسير.

لا تهدف إلى استبدال IDS أو IPS أو SIEM.
🎯 هدفها المساعدة على اتخاذ قرارات أمنية واعية مع الحفاظ على التحكم الكامل.

------------------------------------------------------------

👥 الجمهور المستهدف

👨‍💻 مهندسو أمن الشبكات  
🧑‍✈ محللو SOC  
🔥 مسؤولو الجدران النارية  
🧠 من يرفضون الأتمتة العمياء  

------------------------------------------------------------

📌 الحالة

✔ مستقر  
✔ محدود عن قصد  
✔ متمحور حول اتخاذ القرار  بشكل يدوي ومفهوم 

------------------------------------------------------------

⚠ إخلاء المسؤولية ⚠

يتم توفير هذا البرنامج "كما هو" دون أي ضمان.
لا يتحمل المؤلف أو المساهمون أي مسؤولية عن أي ضرر، فقدان بيانات، أو تأثيرات ناتجة عن استخدام هذه الأداة أو سوء استخدامها.

لا ينفّذ Sentinel-Decide أي إجراء تلقائيًا.
جميع قرارات تطبيق قواعد الجدار الناري تقع على عاتق المستخدم فقط.

استخدامك للأداة يكون على مسؤوليتك الخاصة.



</div>
