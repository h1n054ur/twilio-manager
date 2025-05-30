---
triggers:
  - create skeletons
  - scaffold all class stubs
  - add all menu/usecase/model stubs
agent: CodeActAgent
---

# 1) Load skeletons spec
fetch_spec3{"spec_name":"project_skeletons_spec"}

# 2) Set phase
set_phase3{"phase":"skeletons"}

# 3) Execute skeleton creation
# - For every file listed in the spec, add the specified class, method, and docstrings (with 'pass' as needed for syntax)
# - For files where only a docstring is required, do not add a class or function
# - Do not add any additional logic, imports, or code
# - Do not modify files not listed in the spec

# 4) Log outcome
log_decision3{
  "context":"project-skeletons",
  "decision":"All class/function stubs and docstrings for menus, use cases, and core models were created as per spec. No additional code or logic was added."
}
