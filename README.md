# NHC–AuCl-CREST

> **Automatic workflow for NHC–AuCl complex generation with conformer search (CREST) and optimization (XTB).**

---

## 📖 项目简介

本项目提供了一个 **自动化工作流**，用于从 **NHCs (N-heterocyclic carbene) 分子 SMILES** 出发，构建并优化 **NHC–AuCl 配合物**。  
核心功能包括：

- **SMILES → 3D 构象**（RDKit 预优化）  
- **CREST 构象搜索**（找到最低能量构象）  
- **AuCl 配合物组装**（基于几何方向选择）  
- **XTB 优化**（得到最终稳定结构）  
- **并行化支持**（可同时处理多个分子）


---

## 🔄 工作流程

```mermaid
flowchart TD
    A[CSV 输入: SMILES + ID] --> B[RDKit: 3D 构象生成]
    B --> C[CREST: 构象搜索 & 最低能量构象]
    C --> D[几何学: AuCl 插入]
    D --> E[XTB: 结构优化]
    E --> F[输出结果: XYZ + 日志]
