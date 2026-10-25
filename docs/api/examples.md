# GraphQL: примеры запросов

## Список расходов
```graphql
query {
  expenses(limit: 5, from: "2026-10-01") {
    id
    amount
    comment
    category { name }
  }
}
```
Ответ:
```json
{ "data": { "expenses": [
  { "id": "42", "amount": 350.5, "comment": "Обед", "category": { "name": "Еда" } }
] } }
```

## Добавление расхода
```graphql
mutation {
  addExpense(input: { amount: 350.5, categoryId: "1", comment: "Обед" }) {
    id
    date
  }
}
```

## Сводка за месяц
```graphql
query {
  summary(from: "2026-10-01", to: "2026-10-31") {
    total
    byCategory { category { name } total }
  }
}
```

## Подписка
```graphql
subscription { expenseAdded { id amount category { name } } }
```
