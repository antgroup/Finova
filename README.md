
<div align="center">
  <h1>Finova
</div>
<div align="center">
  <h3>∇ Operable · Verifiable · Agentic</h3>

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

[//]: # ([🌐Website]&#40;https://fineval.readthedocs.io/zh_CN/latest/&#41; |)
[//]: # ([🤗Hugging Face]&#40;https://huggingface.co/datasets/SUFE-AIFLM-Lab/FinEval&#41; |)
[//]: # ([📃Paper]&#40;https://arxiv.org/abs/2308.09975&#41;)

[English](README.md) | [中文](README_zh.md)
</div>

---

While large language models (LLMs) have demonstrated remarkable potential in general domains, their **key capabilities required for deployment in highly complex, rule-bound financial business scenarios**—such as precise tool selection, efficient key information extraction, deep financial reasoning, accurate expression, and compliance safety—have not yet been systematically and scenario-based evaluated.

As agent-based technologies become increasingly integrated into financial business processes, it is critical to establish a **benchmark that closely aligns with real-world financial practices and focuses on the core functions of intelligent agents**.

To this end, we introduce **Finova (Financial Operable and Verifiable Agent Benchmark)**—a **specialized benchmark focused on the core capabilities of financial intelligent agents and challenging financial tasks**.

Unlike benchmarks that emphasize static financial knowledge or general question-answering, our benchmark emphasizes the **key tasks and complex reasoning problems** that LLMs must efficiently and accurately handle as the core component of real-world financial intelligent agent systems.

Finova evaluates models across the following key dimensions:

1. **Agent Tasks**: The ability of the model to perform core tasks in real financial agent applications (including intent recognition, slot filling, tool planning, and expression evaluation).
2. **Complex Reasoning Tasks**: The ability to reason through and professionally answer **complex financial questions annotated by domain experts** and **open-source, verifiable challenging financial problems** (including financial math and coding problems).
3. **Safety & Compliance Detection**: The ability to identify potential compliance risks and security vulnerabilities in **real business scenarios**, ensuring agent operations align with financial regulatory requirements.

**What makes Finova unique is its deep grounding in real-world financial practice: all task designs are based on real industry scenarios and expert annotations.** By carefully integrating real business needs and applying rigorous data processing techniques, we ensure that the evaluation tasks accurately reflect the challenges faced by LLMs in real-world deployment of financial intelligent agent systems.

This benchmark aims to provide financial institutions and developers with a **precise capability measurement tool focused on core agent components**, promoting safe, reliable, and efficient applications of LLMs in handling key and complex financial tasks, and accelerating the practical advancement of financial intelligence.

---

## Why Finova Has Industry-Wide Relevance

- **Core Capabilities Decoupled from Business Logic**  
  We extract **transferable underlying capability modules** (semantic understanding, tool usage, factual consistency, complex reasoning, safety & compliance) from real-world business practices, rather than evaluating specific business logic. Any team building financial agents can use this benchmark to assess foundational capability gaps.

- **Real-World Complexity, Not Academic Simplification**  
  All queries, toolsets, and schemas are constructed based on real user needs and business scenarios, ensuring coverage of **actual application challenges** (e.g., advanced financial math problems, nested regulatory rule scenarios). Compared to synthetic datasets, Finova serves as a more reliable “stress test” environment.

- **Standardized Capability Dimensions for Cross-System Comparison**  
  Toolsets, entity types, and domain designs reflect industry consensus and allow fair comparisons across unified dimensions such as `tool call accuracy`, **`complex reasoning accuracy`**, and `entity recognition F1`.

- **Modular Design for Capability Expansion**  
  - Reasoning capabilities can evolve (e.g., adding **derivative pricing models**, **risk exposure calculations**)
  - Compliance scenarios can be strengthened (e.g., supporting **anti-money laundering rules**, **cross-border regulatory clauses**)
  - Entity/toolsets can expand (e.g., adding bond types, macroeconomic indicator APIs)

---

## 🚀 Who Should Use Finova?

This benchmark is suitable for:

- **Financial AI Product Teams**: Ensure the reliable deployment of intelligent agents in critical business workflows and evaluate their performance in complex financial reasoning and compliance safety scenarios.
- **LLM Developers**: Focus on optimizing deep financial reasoning capabilities, while improving tool call accuracy and compliance risk awareness.
- **Academic Researchers**: Build an agent evaluation environment covering advanced financial reasoning and regulatory safety challenges to drive related technical advancements.
- **Industry Evaluation Agencies**: Establish a cross-platform core capability evaluation standard for financial intelligent agents.


## 🔐 Data Anonymization Notice

To comply with financial data security and privacy requirements, the open-source version of this project has undergone further anonymization. Therefore, **evaluation results based on the open-source version may differ slightly from those in our technical report**. Differences mainly stem from accuracy fluctuations in a few high-sensitivity scenarios, while core capability trends remain consistent.

---

## ⚠️ Disclaimer

Please note: Large language model technology still has limitations. The model outputs involved in this benchmark may contain hallucinations or inaccuracies. All generated content **does not represent the views, positions, or investment advice of Ant Group (or the publisher)**. Given the high timeliness and professionalism of financial information, please consult licensed financial professionals or institutions before making **any investment or business decisions** based on this project.

---