# Project Structure Examples — Before/After

This directory demonstrates the difference between shallow/bad organization and deep/good organization. Focus on the structural difference, not the code content.

---

## TypeScript Example

### Before — Shallow, Technical Layering

```
ecommerce-app/
├── src/
│   ├── services/
│   │   ├── orderService.ts
│   │   ├── inventoryService.ts
│   │   ├── pricingService.ts
│   │   └── monitoringService.ts
│   ├── handlers/
│   │   ├── checkoutHandler.ts
│   │   ├── inventoryHandler.ts
│   │   └── monitoringHandler.ts
│   ├── utils/
│   │   ├── taxCalculator.ts
│   │   ├── discountCalculator.ts
│   │   ├── priceFormatter.ts
│   │   ├── addressParser.ts
│   │   └── currencyParser.ts
│   ├── types/
│   │   ├── orders.ts
│   │   ├── inventory.ts
│   │   ├── pricing.ts
│   │   └── monitoring.ts
│   ├── config/
│   │   ├── app.config.ts
│   │   └── stores.config.ts
│   └── index.ts
├── tests/
│   ├── unit/
│   │   ├── orders.test.ts
│   │   └── inventory.test.ts
│   └── integration/
│       └── e2e.test.ts
├── package.json
└── tsconfig.json
```

**Problems**:
- Related code scattered across `services/`, `handlers/`, `utils/`, `types/`
- Can't find all order processing logic in one place
- File paths don't indicate domain
- 18 files at top level of `src/` — cognitive overload

---

### After — Deep, Conceptual Organization

```
ecommerce-app/
├── src/
│   ├── orders/
│   │   ├── index.ts                 # Public facade (3-5 exports)
│   │   ├── checkout.ts
│   │   ├── fulfillment.ts
│   │   ├── types.ts
│   │   └── utils/
│   │       ├── tax.ts
│   │       └── discounts.ts
│   ├── inventory/
│   │   ├── index.ts
│   │   ├── warehouse.ts
│   │   ├── supplier.ts
│   │   └── types.ts
│   ├── pricing/
│   │   ├── index.ts
│   │   └── fetcher.ts
│   ├── monitoring/
│   │   ├── index.ts
│   │   └── alerts.ts
│   ├── config/
│   │   ├── app.ts
│   │   └── stores.ts
│   └── index.ts
├── tests/
│   └── stack-test/                 # Full-stack tests only
│       ├── orders.test.ts
│       ├── inventory.test.ts
│       └── pricing.test.ts
├── CLAUDE.md                        # Agent contract
├── README.md                        # Overview
├── package.json
└── tsconfig.json
```

**Improvements**:
- Each domain self-contained
- Deep modules: simple `index.ts` facades hide implementation
- Progressive disclosure: domain → module → implementation
- File paths signal domain: `orders/utils/tax.ts`

---

## Python Example

### Before — Shallow, Flat Structure

```
ecommerce_bot/
├── bot.py
├── orders.py
├── inventory.py
├── pricing.py
├── monitoring.py
├── tax_estimator.py
├── discount.py
├── price_fetcher.py
├── alert_sender.py
├── order_processor.py
├── inventory_sync.py
├── store_config.py
├── utils.py
├── constants.py
├── models.py
├── serializers.py
├── validators.py
├── tests/
│   ├── test_orders.py
│   ├── test_inventory.py
│   ├── test_pricing.py
│   └── test_utils.py
├── requirements.txt
└── setup.py
```

**Problems**:
- 20+ files at root — no structure
- No indication of which files belong together
- `utils.py` and `constants.py` become dumping grounds
- Can't navigate without reading everything

---

### After — Deep, Domain-Based Structure

```
ecommerce_bot/
├── src/
│   ├── orders/
│   │   ├── __init__.py             # Public facade
│   │   ├── processor.py
│   │   ├── fulfillment.py
│   │   ├── models.py
│   │   └── utils/
│   │       ├── tax.py
│   │       └── discounts.py
│   ├── inventory/
│   │   ├── __init__.py
│   │   ├── sync.py
│   │   ├── warehouse.py
│   │   └── models.py
│   ├── pricing/
│   │   ├── __init__.py
│   │   └── fetcher.py
│   ├── monitoring/
│   │   ├── __init__.py
│   │   └── alerts.py
│   ├── config/
│   │   ├── __init__.py
│   │   └── stores.py
│   ├── shared/
│   │   ├── constants.py
│   │   └── validators.py
│   └── bot.py
├── tests/
│   └── stack/                      # Full-stack tests
│       ├── test_orders.py
│       └── test_inventory.py
├── CLAUDE.md                        # Agent contract
├── README.md                        # Overview
├── requirements.txt
└── setup.py
```

**Improvements**:
- Clear domain boundaries
- `__init__.py` exports controlled public interface
- Related code co-located
- Easy to discover: start at domain, drill down as needed

---

## Key Differences Summary

| Aspect | Before | After |
|--------|--------|-------|
| **Grouping** | Technical layer (`services/`, `utils/`) | Domain/capability (`orders/`, `inventory/`) |
| **Exports** | 20+ functions, leaking internals | 3-5 exports per module |
| **Discovery** | Flat or scattered | Progressive disclosure |
| **Navigation** | File paths meaningless | File paths signal domain |
| **Testing** | Unit/integration split | Stack tests at domain boundaries |

---

## See Also

- @docs/L0-foundation.md — Deep modules, progressive disclosure, conceptual organization
- @docs/L1-feedback-loops.md — Stack tests at module boundaries
- @docs/L2-behavioral-guardrails.md — Skills that enforce structural conventions
