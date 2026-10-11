# batch-eval-guide.md

单条仅作烟雾测试。冻结正式样本，记录模型/系统版本、输入、参数、失败与重试，记录实际账单；不得把调试集结果当泛化结论。用 scripts/audit_results.py 审计完整集合和待裁定项。
