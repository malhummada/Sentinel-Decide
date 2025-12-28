Sentinel-Decide

Sentinel-Decide is a human-guided decision engine for Suricata alerts.
It analyzes Suricata eve.json, groups alerts into incidents, proposes defensive decisions, and optionally exports nftables rules without enforcing anything automatically.

The goal is simple:
observe → analyze → propose → let the human decide.

Why Sentinel-Decide exists

Modern IDS systems generate a large number of alerts.
Blind automation is dangerous, but manual analysis does not scale.

Sentinel-Decide sits between detection and enforcement:

It does not replace Suricata

It does not act as a firewall

It does not auto-block traffic

It helps operators decide

What it does

Reads Suricata eve.json

Filters non-actionable informational alerts

Groups alerts by time window, source, and behavior

Builds higher-level incidents

Proposes decisions:

observe

rate_limit

block

Aggregates decisions per source

Exports reviewable nftables rules

Asks the user before copying or applying any rule

What it does NOT do

No automatic enforcement

No background daemon

No changes to Suricata configuration

No machine learning

No promises of “AI security”

This tool keeps humans in the loop.

Requirements

Python 3.9+

Suricata with eve.json enabled

nftables (optional, only for rule export/apply)

Linux system

Project structure
Sentinel-Decide/
├── explainer/
│   ├── incident_builder.py
│   ├── decision_engine.py
│   ├── decision_aggregator.py
│   └── nftables_file_exporter.py
├── tools/
│   └── run_pipeline.py
├── output/
│   └── (generated files)
└── README.md

Usage
Automatic (last 5 minutes)
python3 -m tools.run_pipeline auto

Last N minutes / hours / days
python3 -m tools.run_pipeline last 5m
python3 -m tools.run_pipeline last 2h
python3 -m tools.run_pipeline last 1d

Since a specific date
python3 -m tools.run_pipeline since 2025-12-20

Between two dates
python3 -m tools.run_pipeline between 2025-12-20 2025-12-27

Explicit timestamps
python3 -m tools.run_pipeline 2025-12-27T02:40:00 2025-12-28T02:45:00

nftables integration

When actionable decisions exist, Sentinel-Decide:

Generates an nftables rules file

Shows the file path

Asks the user:

[1] Do nothing
[2] Copy to /etc/nftables.d/
[3] Copy and apply now


Nothing is applied without explicit confirmation.

Output files

Generated under output/:

incidents.json – grouped incidents

decisions.json – per-incident decisions

decision_summary.json – aggregated decisions

cyphorn-guard.nft – nftables rules (if any)

Design philosophy

Deterministic logic

Explainable decisions

Minimal assumptions

Safe-by-default

Human-first security

Intended audience

Network security engineers

SOC analysts

Firewall administrators

People who distrust blind automation

Status

This project is stable and intentionally limited.
Future changes will focus on clarity, not complexity.

License

To be defined.

Sentinel-Decide (العربية)

Sentinel-Decide هو محرك اقتراح قرارات مبني لمساعدة محللي الأمن عند التعامل مع تنبيهات Suricata.

المشروع لا يقوم بالمنع التلقائي، ولا يفرض أي إجراء.
هو أداة تحليل واقتراح، والقرار النهائي دائمًا بيد الإنسان.

لماذا Sentinel-Decide؟

أنظمة IDS تولد آلاف التنبيهات.
الأتمتة الكاملة خطيرة، والتحليل اليدوي بطيء.

Sentinel-Decide يعمل كطبقة وسطى:

مراقبة → تحليل → اقتراح → قرار بشري

ماذا يفعل؟

يقرأ ملف eve.json الخاص بـ Suricata

يستبعد التنبيهات غير المهمة

يجمع التنبيهات في حوادث منطقية

يقترح إجراء مناسب:

مراقبة فقط

تحديد معدل

حظر مؤقت

يولد قواعد nftables قابلة للمراجعة

لا يطبق أي شيء بدون موافقة المستخدم

ماذا لا يفعل؟

لا يمنع تلقائيًا

لا يعدل إعدادات Suricata

لا يعمل كخدمة دائمة

لا يستخدم AI أو ML

لا يدعي الحماية المطلقة

المتطلبات

Python 3.9 أو أحدث

Suricata مع تفعيل eve.json

nftables (اختياري)

نظام Linux

طريقة الاستخدام
تلقائي (آخر 5 دقائق)
python3 -m tools.run_pipeline auto

آخر مدة زمنية
python3 -m tools.run_pipeline last 10m
python3 -m tools.run_pipeline last 2h
python3 -m tools.run_pipeline last 1d

من تاريخ حتى الآن
python3 -m tools.run_pipeline since 2025-12-20

بين تاريخين
python3 -m tools.run_pipeline between 2025-12-20 2025-12-27

قواعد nftables

عند وجود قرارات قابلة للتنفيذ:

يتم إنشاء ملف قواعد فقط

يُطلب من المستخدم الاختيار:

عدم التنفيذ

النسخ فقط

النسخ والتنفيذ

لا يتم أي تغيير بدون تأكيد صريح.

فلسفة التصميم

قرارات قابلة للتفسير

تحكم كامل بيد الإنسان

أمان افتراضي

بساطة ووضوح

لمن هذا المشروع؟

مهندسو الشبكات

محللو SOC

مسؤولو الجدران النارية

من يرفض الأتمتة العمياء

الحالة

المشروع مكتمل وظيفيًا، ومحدود عن قصد.
أي تطوير مستقبلي سيكون مدروسًا وبسيطًا.