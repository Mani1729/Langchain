# LangChain Barber Agent - Interview Questions (100 Questions)

## Architecture & Design (1-20)

1. **How does the barber agent demonstrate middleware patterns?**

2. **What are the key components of the barber agent architecture?**

3. **Describe the relationship between LangGraph and middleware.**

4. **Why is middleware useful for this barbershop use case?**

5. **How does human-in-the-loop improve the booking experience?**

6. **Explain the middleware stack composition order.**

7. **What are the advantages of middleware over hard-coded logic?**

8. **How do middlewares communicate state to each other?**

9. **Describe the tool execution flow through middlewares.**

10. **Why is business logic in middleware instead of tools?**

11. **How does the system handle concurrent booking requests?**

12. **Explain the database interaction patterns.**

13. **What role does Chainlit play in this system?**

14. **How does the system maintain consistency?**

15. **Describe the error recovery mechanisms.**

16. **What are the extensibility points?**

17. **How would you add new services/features?**

18. **Explain the testing strategy.**

19. **What performance considerations apply?**

20. **How does this system scale?**

## Middleware Stack Implementation (21-50)

21. **What is the purpose of BusinessRules middleware?**

22. **Describe the 2-hour booking notice rule.**

23. **Explain the 24-hour cancellation policy.**

24. **How does BusinessRules validate constraints?**

25. **What happens when a rule is violated?**

26. **How does ConversationSummary middleware work?**

27. **When is conversation summarization triggered?**

28. **What information is preserved in summaries?**

29. **How does summarization affect context window?**

30. **What is the PII masking strategy?**

31. **How does email masking work?**

32. **Describe credit card number masking.**

33. **How do you prevent data exposure in logs?**

34. **What other PII should be masked?**

35. **What is UsageTracking middleware?**

36. **How is token usage calculated?**

37. **What metrics are tracked?**

38. **How is usage data used?**

39. **Explain the HumanInTheLoop middleware.**

40. **When is human approval required?**

41. **How does the user approve operations?**

42. **What information is presented to humans?**

43. **How do you handle approval timeouts?**

44. **What happens on approval denial?**

45. **How are middlewares tested in isolation?**

46. **Describe integration testing of middleware.**

47. **How do you debug middleware issues?**

48. **What metrics indicate middleware performance?**

49. **How would you add a new middleware?**

50. **What are common middleware pitfalls?**

## Tool Design & Implementation (51-75)

51. **How many custom tools are implemented?**

52. **Describe the check_availability tool.**

53. **What parameters does each tool accept?**

54. **How is tool discovery implemented?**

55. **Explain tool description for LLM understanding.**

56. **How are tool results validated?**

57. **What error handling exists for tool failures?**

58. **Describe the create_booking tool.**

59. **Why does create_booking require HITL?**

60. **How is availability verified during booking?**

61. **Explain conflict detection for bookings.**

62. **What happens on booking success/failure?**

63. **Describe the modify_booking tool.**

64. **How does the system handle rebooking?**

65. **Explain the cancel_booking tool.**

66. **How is the cancellation deadline enforced?**

67. **What refund logic is implemented?**

68. **Describe the get_barbers tool.**

69. **How is barber availability calculated?**

70. **Explain specialties filtering.**

71. **Describe the get_services tool.**

72. **How are services priced?**

73. **Explain the lookup_customer tool.**

74. **How is customer history tracked?**

75. **Describe the check_policies tool.**

## Database & ORM (76-90)

76. **What database schema is used?**

77. **Describe the customers table.**

78. **Explain the barbers table structure.**

79. **What fields are in the services table?**

80. **Describe the bookings table.**

81. **What is the business_rules table?**

82. **How are relationships modeled?**

83. **Explain foreign key constraints.**

84. **How are indexes optimized?**

85. **Describe the migration strategy.**

86. **What Alembic migrations exist?**

87. **How are schema changes handled?**

88. **Explain transaction handling.**

89. **What consistency models are used?**

90. **How is data integrity ensured?**

## API Design & FastAPI (91-110)

91. **What REST endpoints are exposed?**

92. **Describe the booking creation endpoint.**

93. **How is request validation handled?**

94. **Explain response serialization.**

95. **What HTTP status codes are used?**

96. **How are errors returned to clients?**

97. **Explain authentication on endpoints.**

98. **What rate limiting is implemented?**

99. **How is CORS configured?**

100. **Describe the API documentation.**

## Answer Guide

**Key Topics**: Middleware architecture, Human-in-the-loop workflows, Business rules enforcement, Tool design, Database schema, API design, Production patterns

## Model Answers (1-100)

1. Implement it as a pipeline: validate input, apply domain rules, execute the operation, and add retries, timeouts, and fallbacks for resilience.

2. It is a core concept used to make the system predictable and maintainable; explain its role in the end-to-end flow and where it adds value.

3. Model the workflow as explicit state transitions between nodes with conditional edges, bounded retries, and checkpointing for resumability.

4. It is chosen to improve accuracy, reliability, and developer velocity; also mention the trade-off in complexity or operational overhead.

5. Implement it as a pipeline: validate input, apply domain rules, execute the operation, and add retries, timeouts, and fallbacks for resilience.

6. Define clear responsibilities for agents/tools, enforce guardrails around side effects, and use middleware for observability and policy control.

7. It is a core concept used to make the system predictable and maintainable; explain its role in the end-to-end flow and where it adds value.

8. Model the workflow as explicit state transitions between nodes with conditional edges, bounded retries, and checkpointing for resumability.

9. Define clear responsibilities for agents/tools, enforce guardrails around side effects, and use middleware for observability and policy control.

10. It is chosen to improve accuracy, reliability, and developer velocity; also mention the trade-off in complexity or operational overhead.

11. Implement it as a pipeline: validate input, apply domain rules, execute the operation, and add retries, timeouts, and fallbacks for resilience.

12. Use schema-aware generation and validation, parameterized execution, and dialect-safe adapters to keep queries correct, secure, and portable.

13. Use a clear architecture-first explanation, then mention trade-offs, reliability controls, and measurable outcomes.

14. Implement it as a pipeline: validate input, apply domain rules, execute the operation, and add retries, timeouts, and fallbacks for resilience.

15. Use a clear architecture-first explanation, then mention trade-offs, reliability controls, and measurable outcomes.

16. It is a core concept used to make the system predictable and maintainable; explain its role in the end-to-end flow and where it adds value.

17. Implement it as a pipeline: validate input, apply domain rules, execute the operation, and add retries, timeouts, and fallbacks for resilience.

18. Use layered testing (unit, integration, E2E), regression datasets, and trace-driven debugging to quickly isolate root causes.

19. Improve performance with caching, batching, async/parallel execution, and bottleneck tracing, then validate gains with percentile latency metrics.

20. Implement it as a pipeline: validate input, apply domain rules, execute the operation, and add retries, timeouts, and fallbacks for resilience.

21. It is a core concept used to make the system predictable and maintainable; explain its role in the end-to-end flow and where it adds value.

22. Use a clear architecture-first explanation, then mention trade-offs, reliability controls, and measurable outcomes.

23. Use a clear architecture-first explanation, then mention trade-offs, reliability controls, and measurable outcomes.

24. Implement it as a pipeline: validate input, apply domain rules, execute the operation, and add retries, timeouts, and fallbacks for resilience.

25. Use a clear architecture-first explanation, then mention trade-offs, reliability controls, and measurable outcomes.

26. Implement it as a pipeline: validate input, apply domain rules, execute the operation, and add retries, timeouts, and fallbacks for resilience.

27. Use a clear architecture-first explanation, then mention trade-offs, reliability controls, and measurable outcomes.

28. Use a clear architecture-first explanation, then mention trade-offs, reliability controls, and measurable outcomes.

29. Implement it as a pipeline: validate input, apply domain rules, execute the operation, and add retries, timeouts, and fallbacks for resilience.

30. It is a core concept used to make the system predictable and maintainable; explain its role in the end-to-end flow and where it adds value.

31. Implement it as a pipeline: validate input, apply domain rules, execute the operation, and add retries, timeouts, and fallbacks for resilience.

32. Use a clear architecture-first explanation, then mention trade-offs, reliability controls, and measurable outcomes.

33. Implement it as a pipeline: validate input, apply domain rules, execute the operation, and add retries, timeouts, and fallbacks for resilience.

34. Apply least privilege, strict validation, secret vaulting, encryption, and audit trails, then enforce policy checks before side effects.

35. It is a core concept used to make the system predictable and maintainable; explain its role in the end-to-end flow and where it adds value.

36. Use a clear architecture-first explanation, then mention trade-offs, reliability controls, and measurable outcomes.

37. Use CI/CD with staged promotion and rollback readiness, then monitor errors, latency, cost, and quality signals with actionable alerts.

38. Use a clear architecture-first explanation, then mention trade-offs, reliability controls, and measurable outcomes.

39. Define clear responsibilities for agents/tools, enforce guardrails around side effects, and use middleware for observability and policy control.

40. Design UI state flow for responsiveness and resilience, and enforce type-safe contracts between components and backend streams.

41. Implement it as a pipeline: validate input, apply domain rules, execute the operation, and add retries, timeouts, and fallbacks for resilience.

42. Use a clear architecture-first explanation, then mention trade-offs, reliability controls, and measurable outcomes.

43. Implement it as a pipeline: validate input, apply domain rules, execute the operation, and add retries, timeouts, and fallbacks for resilience.

44. Use a clear architecture-first explanation, then mention trade-offs, reliability controls, and measurable outcomes.

45. Use layered testing (unit, integration, E2E), regression datasets, and trace-driven debugging to quickly isolate root causes.

46. Use layered testing (unit, integration, E2E), regression datasets, and trace-driven debugging to quickly isolate root causes.

47. Implement it as a pipeline: validate input, apply domain rules, execute the operation, and add retries, timeouts, and fallbacks for resilience.

48. Improve performance with caching, batching, async/parallel execution, and bottleneck tracing, then validate gains with percentile latency metrics.

49. Implement it as a pipeline: validate input, apply domain rules, execute the operation, and add retries, timeouts, and fallbacks for resilience.

50. It is a core concept used to make the system predictable and maintainable; explain its role in the end-to-end flow and where it adds value.

51. Define clear responsibilities for agents/tools, enforce guardrails around side effects, and use middleware for observability and policy control.

52. Define clear responsibilities for agents/tools, enforce guardrails around side effects, and use middleware for observability and policy control.

53. Define clear responsibilities for agents/tools, enforce guardrails around side effects, and use middleware for observability and policy control.

54. Define clear responsibilities for agents/tools, enforce guardrails around side effects, and use middleware for observability and policy control.

55. Define clear responsibilities for agents/tools, enforce guardrails around side effects, and use middleware for observability and policy control.

56. Define clear responsibilities for agents/tools, enforce guardrails around side effects, and use middleware for observability and policy control.

57. Define clear responsibilities for agents/tools, enforce guardrails around side effects, and use middleware for observability and policy control.

58. Define clear responsibilities for agents/tools, enforce guardrails around side effects, and use middleware for observability and policy control.

59. It is chosen to improve accuracy, reliability, and developer velocity; also mention the trade-off in complexity or operational overhead.

60. Use a clear architecture-first explanation, then mention trade-offs, reliability controls, and measurable outcomes.

61. Use a clear architecture-first explanation, then mention trade-offs, reliability controls, and measurable outcomes.

62. Use a clear architecture-first explanation, then mention trade-offs, reliability controls, and measurable outcomes.

63. Define clear responsibilities for agents/tools, enforce guardrails around side effects, and use middleware for observability and policy control.

64. Implement it as a pipeline: validate input, apply domain rules, execute the operation, and add retries, timeouts, and fallbacks for resilience.

65. Define clear responsibilities for agents/tools, enforce guardrails around side effects, and use middleware for observability and policy control.

66. Use a clear architecture-first explanation, then mention trade-offs, reliability controls, and measurable outcomes.

67. Use a clear architecture-first explanation, then mention trade-offs, reliability controls, and measurable outcomes.

68. Define clear responsibilities for agents/tools, enforce guardrails around side effects, and use middleware for observability and policy control.

69. Use a clear architecture-first explanation, then mention trade-offs, reliability controls, and measurable outcomes.

70. Use a clear architecture-first explanation, then mention trade-offs, reliability controls, and measurable outcomes.

71. Define clear responsibilities for agents/tools, enforce guardrails around side effects, and use middleware for observability and policy control.

72. Use a clear architecture-first explanation, then mention trade-offs, reliability controls, and measurable outcomes.

73. Define clear responsibilities for agents/tools, enforce guardrails around side effects, and use middleware for observability and policy control.

74. Use a clear architecture-first explanation, then mention trade-offs, reliability controls, and measurable outcomes.

75. Define clear responsibilities for agents/tools, enforce guardrails around side effects, and use middleware for observability and policy control.

76. Use schema-aware generation and validation, parameterized execution, and dialect-safe adapters to keep queries correct, secure, and portable.

77. Use a clear architecture-first explanation, then mention trade-offs, reliability controls, and measurable outcomes.

78. Use a clear architecture-first explanation, then mention trade-offs, reliability controls, and measurable outcomes.

79. Use a clear architecture-first explanation, then mention trade-offs, reliability controls, and measurable outcomes.

80. Use a clear architecture-first explanation, then mention trade-offs, reliability controls, and measurable outcomes.

81. It is a core concept used to make the system predictable and maintainable; explain its role in the end-to-end flow and where it adds value.

82. Use a clear architecture-first explanation, then mention trade-offs, reliability controls, and measurable outcomes.

83. Use a clear architecture-first explanation, then mention trade-offs, reliability controls, and measurable outcomes.

84. Improve performance with caching, batching, async/parallel execution, and bottleneck tracing, then validate gains with percentile latency metrics.

85. Use a clear architecture-first explanation, then mention trade-offs, reliability controls, and measurable outcomes.

86. Use a clear architecture-first explanation, then mention trade-offs, reliability controls, and measurable outcomes.

87. Use a clear architecture-first explanation, then mention trade-offs, reliability controls, and measurable outcomes.

88. Use a clear architecture-first explanation, then mention trade-offs, reliability controls, and measurable outcomes.

89. Use a clear architecture-first explanation, then mention trade-offs, reliability controls, and measurable outcomes.

90. Use a clear architecture-first explanation, then mention trade-offs, reliability controls, and measurable outcomes.

91. Use a clear architecture-first explanation, then mention trade-offs, reliability controls, and measurable outcomes.

92. Use a clear architecture-first explanation, then mention trade-offs, reliability controls, and measurable outcomes.

93. Use a clear architecture-first explanation, then mention trade-offs, reliability controls, and measurable outcomes.

94. Use a clear architecture-first explanation, then mention trade-offs, reliability controls, and measurable outcomes.

95. Use a clear architecture-first explanation, then mention trade-offs, reliability controls, and measurable outcomes.

96. Use a clear architecture-first explanation, then mention trade-offs, reliability controls, and measurable outcomes.

97. Apply least privilege, strict validation, secret vaulting, encryption, and audit trails, then enforce policy checks before side effects.

98. Use a clear architecture-first explanation, then mention trade-offs, reliability controls, and measurable outcomes.

99. Use a clear architecture-first explanation, then mention trade-offs, reliability controls, and measurable outcomes.

100. Use a clear architecture-first explanation, then mention trade-offs, reliability controls, and measurable outcomes.

