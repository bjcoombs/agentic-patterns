# Project Structure Examples — Before/After

This directory demonstrates the difference between shallow/bad organization and deep/good organization. Focus on the structural difference, not the code content.

---

## TypeScript Example

### Before — Shallow, Technical Layering

```
trading-app/
├── src/
│   ├── services/
│   │   ├── tradingService.ts
│   │   ├── bridgeService.ts
│   │   ├── oracleService.ts
│   │   └── monitoringService.ts
│   ├── handlers/
│   │   ├── tradeHandler.ts
│   │   ├── bridgeHandler.ts
│   │   └── monitoringHandler.ts
│   ├── utils/
│   │   ├── gasCalculator.ts
│   │   ├── slippageCalculator.ts
│   │   ├── priceFormatter.ts
│   │   ├── addressParser.ts
│   │   └── chainIdParser.ts
│   ├── types/
│   │   ├── trading.ts
│   │   ├── bridging.ts
│   │   ├── oracle.ts
│   │   └── monitoring.ts
│   ├── config/
│   │   ├── app.config.ts
│   │   └── chains.config.ts
│   └── index.ts
├── tests/
│   ├── unit/
│   │   ├── trading.test.ts
│   │   └── bridging.test.ts
│   └── integration/
│       └── e2e.test.ts
├── package.json
└── tsconfig.json
```

**Problems**:
- Related code scattered across `services/`, `handlers/`, `utils/`, `types/`
- Can't find all trading logic in one place
- File paths don't indicate domain
- 18 files at top level of `src/` — cognitive overload

---

### After — Deep, Conceptual Organization

```
trading-app/
├── src/
│   ├── trading/
│   │   ├── index.ts                 # Public facade (3-5 exports)
│   │   ├── execute.ts
│   │   ├── monitor.ts
│   │   ├── types.ts
│   │   └── utils/
│   │       ├── gas.ts
│   │       └── slippage.ts
│   ├── bridging/
│   │   ├── index.ts
│   │   ├── wormhole.ts
│   │   ├── layerzero.ts
│   │   └── types.ts
│   ├── oracle/
│   │   ├── index.ts
│   │   └── fetcher.ts
│   ├── monitoring/
│   │   ├── index.ts
│   │   └── alerts.ts
│   ├── config/
│   │   ├── app.ts
│   │   └── chains.ts
│   └── index.ts
├── tests/
│   └── stack-test/                 # Full-stack tests only
│       ├── trading.test.ts
│       ├── bridging.test.ts
│       └── oracle.test.ts
├── CLAUDE.md                        # Agent contract
├── README.md                        # Overview
├── package.json
└── tsconfig.json
```

**Improvements**:
- Each domain self-contained
- Deep modules: simple `index.ts` facades hide implementation
- Progressive disclosure: domain → module → implementation
- File paths signal domain: `trading/utils/gas.ts`

---

## Python Example

### Before — Shallow, Flat Structure

```
trading_bot/
├── bot.py
├── trading.py
├── bridging.py
├── oracle.py
├── monitoring.py
├── gas_estimator.py
├── slippage.py
├── price_fetcher.py
├── alert_sender.py
├── trade_executor.py
├── bridge_router.py
├── chain_config.py
├── utils.py
├── constants.py
├── models.py
├── serializers.py
├── validators.py
├── tests/
│   ├── test_trading.py
│   ├── test_bridging.py
│   ├── test_oracle.py
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
trading_bot/
├── src/
│   ├── trading/
│   │   ├── __init__.py             # Public facade
│   │   ├── executor.py
│   │   ├── monitor.py
│   │   ├── models.py
│   │   └── utils/
│   │       ├── gas.py
│   │       └── slippage.py
│   ├── bridging/
│   │   ├── __init__.py
│   │   ├── router.py
│   │   ├── wormhole.py
│   │   └── models.py
│   ├── oracle/
│   │   ├── __init__.py
│   │   └── fetcher.py
│   ├── monitoring/
│   │   ├── __init__.py
│   │   └── alerts.py
│   ├── config/
│   │   ├── __init__.py
│   │   └── chains.py
│   ├── shared/
│   │   ├── constants.py
│   │   └── validators.py
│   └── bot.py
├── tests/
│   └── stack/                      # Full-stack tests
│       ├── test_trading.py
│       └── test_bridging.py
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
| **Grouping** | Technical layer (`services/`, `utils/`) | Domain/capability (`trading/`, `bridging/`) |
| **Exports** | 20+ functions, leaking internals | 3-5 exports per module |
| **Discovery** | Flat or scattered | Progressive disclosure |
| **Navigation** | File paths meaningless | File paths signal domain |
| **Testing** | Unit/integration split | Stack tests at domain boundaries |

---

## See Also

- @docs/L0-foundation.md — Deep modules, progressive disclosure, conceptual organization
- @docs/L1-feedback-loops.md — Stack tests at module boundaries
- @docs/L2-behavioral-guardrails.md — Skills that enforce structural conventions
