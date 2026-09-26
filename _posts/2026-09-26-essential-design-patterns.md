---
layout: post
title: "Essential Software Design Patterns: Architectural Principles and Multi-Language Implementations"
date: 2026-09-26
categories: [Technology, Software Engineering]
tags: [Design Patterns, Software Architecture, Python, Java, C++, Clean Code, Object-Oriented Programming]
---

Design patterns offer proven, language-agnostic blueprints for solving recurring software engineering challenges. While the underlying architectural principles remain universal, their concrete implementations vary meaningfully depending on each language's type system, memory model, and native language features.

Here is a practical, code-first guide to ten essential design patterns—beginning with **Singleton**, **Flyweight**, **Observer**, and **Registry**—featuring side-by-side implementations in **Python**, **Java**, and **C++**.

<!--more-->

---

## Quick Reference: Pattern Classification

| Pattern | Category | Primary Intent | Language-Specific Idioms |
|:---|:---|:---|:---|
| **Singleton** | Creational | Guarantee a single global instance of a class | **Python:** Metaclass / Module<br>**Java:** Bill Pugh Holder idiom / `enum`<br>**C++:** Meyers' Singleton (`static` local) |
| **Flyweight** | Structural | Drastically cut memory usage by sharing immutable intrinsic state | **Python:** Factory + `__slots__`<br>**Java:** `record` + `ConcurrentHashMap`<br>**C++:** `std::shared_ptr<const T>` pool |
| **Observer** | Behavioral | Decoupled one-to-many publish-subscribe event notification | **Python:** Listener lists / callables<br>**Java:** `@FunctionalInterface` + `CopyOnWriteArrayList`<br>**C++:** `std::vector<std::weak_ptr<Observer>>` |
| **Registry** | Creational | Centralized catalog mapping string keys to constructors/factories | **Python:** Decorator / `__init_subclass__`<br>**Java:** `Map<String, Supplier<T>>`<br>**C++:** Static map of factory lambdas |
| **Factory Method** | Creational | Delegate object instantiation without binding to concrete classes | **Python:** Dynamic callable dispatch<br>**Java:** Interface + switch expressions<br>**C++:** `std::unique_ptr<Base>` return |
| **Builder** | Creational | Construct complex multi-attribute objects step-by-step | **Python / Java / C++:** Method chaining / Fluent API |
| **Adapter** | Structural | Convert incompatible interfaces to match what client expects | **Python / Java / C++:** Wrapper composition / delegation |
| **Decorator** | Structural | Attach behavior to objects dynamically at runtime without subclassing | **Python / Java / C++:** Wrapper composition matching base interface |
| **Strategy** | Behavioral | Encapsulate interchangeable algorithms selected at runtime | **Python / Java:** First-class functions / `@FunctionalInterface` lambdas<br>**C++:** `std::function` or strategy class |
| **Chain of Responsibility** | Behavioral | Pass requests sequentially through a pipeline of handlers | **Python / Java / C++:** Linked handler list / middleware pipeline |

---

## 1. The Singleton Pattern (Creational)

### Core Concept & Intent
The **Singleton Pattern** ensures that a class has only one instance while providing a global access point to it. It is commonly employed for connection pools, logging managers, thread pools, and hardware controllers.

### Structural Architecture
```text
┌──────────────────────────────────────┐
│           Singleton Class            │
├──────────────────────────────────────┤
│ - static instance: Singleton         │
│ - constructor() [Private / Hidden]   │
├──────────────────────────────────────┤
│ + static getInstance(): Singleton    │
│ + executeOperation(): void           │
└──────────────────────────────────────┘
```

### Multi-Language Implementations

#### Python (Thread-Safe Metaclass)
```python
import threading
from typing import Any, Dict


class SingletonMeta(type):
    """Thread-safe Singleton metaclass using double-checked locking."""
    _instances: Dict[type, Any] = {}
    _lock: threading.Lock = threading.Lock()

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class DatabasePool(metaclass=SingletonMeta):
    def __init__(self, dsn: str = "postgresql://localhost:5432/app") -> None:
        self.dsn = dsn

    def query(self, sql: str) -> str:
        return f"Querying '{sql}' on {self.dsn}"


# Usage
db1 = DatabasePool()
db2 = DatabasePool()
assert db1 is db2  # Exactly the same instance in memory
```

#### Java (Bill Pugh Singleton / Initialization-on-Demand Holder)
```java
public class DatabasePool {
    private final String dsn;

    // Private constructor prevents direct instantiation
    private DatabasePool() {
        this.dsn = "postgresql://localhost:5432/app";
    }

    // Bill Pugh idiom: Thread-safe, lazily initialized on first access without synchronization overhead
    private static class Holder {
        private static final DatabasePool INSTANCE = new DatabasePool();
    }

    public static DatabasePool getInstance() {
        return Holder.INSTANCE;
    }

    public String query(String sql) {
        return "Querying '" + sql + "' on " + dsn;
    }
}

// Usage
DatabasePool db1 = DatabasePool.getInstance();
DatabasePool db2 = DatabasePool.getInstance();
System.out.println(db1 == db2); // true (identical reference)
```

#### C++ (Meyers' Singleton)
```cpp
#include <iostream>
#include <string>

class DatabasePool {
public:
    // Delete copy and move semantics to enforce single instance
    DatabasePool(const DatabasePool&) = delete;
    DatabasePool& operator=(const DatabasePool&) = delete;
    DatabasePool(DatabasePool&&) = delete;
    DatabasePool& operator=(DatabasePool&&) = delete;

    // Thread-safe in C++11 and later (static local initialization is atomic)
    static DatabasePool& getInstance() {
        static DatabasePool instance("postgresql://localhost:5432/app");
        return instance;
    }

    void query(const std::string& sql) const {
        std::cout << "Executing '" << sql << "' on " << dsn_ << "\n";
    }

private:
    explicit DatabasePool(std::string dsn) : dsn_(std::move(dsn)) {}
    std::string dsn_;
};

// Usage
int main() {
    DatabasePool& db1 = DatabasePool::getInstance();
    DatabasePool& db2 = DatabasePool::getInstance();
    // &db1 == &db2 (Identical memory address)
    return 0;
}
```

---

## 2. The Flyweight Pattern (Structural)

### Core Concept & Intent
The **Flyweight Pattern** reduces memory footprint by sharing common, immutable state across thousands or millions of fine-grained objects. State is separated into:
* **Intrinsic State:** Context-independent, immutable data stored inside the shared Flyweight (e.g., symbol, exchange, currency).
* **Extrinsic State:** Context-dependent, mutable data passed in from the client (e.g., order ID, timestamp, volume, execution price).

### Structural Architecture
```text
┌─────────────────────────────────┐
│        FlyweightFactory         │ ◄── Caches & shares unique flyweights
├─────────────────────────────────┤
│ - cache: map<key, Flyweight>    │
├─────────────────────────────────┤
│ + get(symbol, exchange): FW     │
└────────────────▲────────────────┘
                 │ references
┌────────────────┴────────────────┐       ┌───────────────────────────────┐
│     Flyweight (Metadata)        │       │       Context (Order)         │
├─────────────────────────────────┤       ├───────────────────────────────┤
│ + symbol: string   (Intrinsic)  │◄──────┼─+ security: Flyweight         │
│ + exchange: string (Intrinsic)  │       │ + orderId: int    (Extrinsic) │
│ + currency: string (Intrinsic)  │       │ + price: float    (Extrinsic) │
└─────────────────────────────────┘       └───────────────────────────────┘
```

### Multi-Language Implementations

#### Python
```python
from dataclasses import dataclass
from typing import Dict, Tuple


@dataclass(frozen=True, slots=True)
class SecurityMetadata:
    """Intrinsic State: Immutable and shared across millions of orders."""
    symbol: str
    exchange: str
    currency: str


class SecurityFlyweightFactory:
    """Factory managing the pool of unique Flyweight instances."""
    _pool: Dict[Tuple[str, str], SecurityMetadata] = {}

    @classmethod
    def get(cls, symbol: str, exchange: str, currency: str) -> SecurityMetadata:
        key = (symbol.upper(), exchange.upper())
        if key not in cls._pool:
            cls._pool[key] = SecurityMetadata(
                symbol=symbol.upper(),
                exchange=exchange.upper(),
                currency=currency.upper(),
            )
        return cls._pool[key]


class Order:
    """Extrinsic Context: Stores specific transaction state + Flyweight pointer."""
    __slots__ = ("order_id", "security", "price", "shares")

    def __init__(
        self,
        order_id: int,
        security: SecurityMetadata,
        price: float,
        shares: int,
    ) -> None:
        self.order_id = order_id
        self.security = security  # Pointer to shared Flyweight
        self.price = price
        self.shares = shares


# Usage: 100,000 orders share exactly ONE metadata object
aapl_meta = SecurityFlyweightFactory.get("AAPL", "NASDAQ", "USD")
orders = [
    Order(order_id=i, security=aapl_meta, price=180.0, shares=50)
    for i in range(100_000)
]
assert orders[0].security is orders[99999].security
```

#### Java (Immutable Record + ConcurrentHashMap)
```java
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

// Flyweight: Immutable record holding intrinsic state
public record SecurityMetadata(String symbol, String exchange, String currency) {}

public class SecurityFlyweightFactory {
    private static final Map<String, SecurityMetadata> POOL = new ConcurrentHashMap<>();

    public static SecurityMetadata get(String symbol, String exchange, String currency) {
        String key = (symbol + ":" + exchange).toUpperCase();
        return POOL.computeIfAbsent(key, k -> new SecurityMetadata(
            symbol.toUpperCase(), exchange.toUpperCase(), currency.toUpperCase()
        ));
    }
}

public class Order {
    private final int orderId;
    private final SecurityMetadata security; // Pointer to shared Flyweight
    private double price;
    private int quantity;

    public Order(int orderId, SecurityMetadata security, double price, int quantity) {
        this.orderId = orderId;
        this.security = security;
        this.price = price;
        this.quantity = quantity;
    }

    public SecurityMetadata getSecurity() { return security; }
}

// Usage: 100,000 orders share exactly ONE metadata record in heap
SecurityMetadata meta = SecurityFlyweightFactory.get("AAPL", "NASDAQ", "USD");
Order o1 = new Order(1, meta, 185.5, 100);
Order o2 = new Order(2, meta, 186.0, 200);
System.out.println(o1.getSecurity() == o2.getSecurity()); // true (same reference)
```

#### C++
```cpp
#include <iostream>
#include <memory>
#include <string>
#include <unordered_map>

struct SecurityMetadata {
    const std::string symbol;
    const std::string exchange;
    const std::string currency;
};

class SecurityFlyweightFactory {
public:
    static std::shared_ptr<const SecurityMetadata> get(const std::string& symbol, const std::string& exchange, const std::string& currency) {
        std::string key = symbol + ":" + exchange;
        auto it = pool_.find(key);
        if (it == pool_.end()) {
            auto meta = std::make_shared<const SecurityMetadata>(SecurityMetadata{symbol, exchange, currency});
            pool_[key] = meta;
            return meta;
        }
        return it->second;
    }

private:
    static inline std::unordered_map<std::string, std::shared_ptr<const SecurityMetadata>> pool_;
};

struct Order {
    int orderId;
    std::shared_ptr<const SecurityMetadata> security; // Shared pointer to flyweight
    double price;
    int quantity;
};
```

---

## 3. The Observer Pattern (Behavioral)

### Core Concept & Intent
The **Observer Pattern** defines a one-to-many relationship where a core subject (publisher) automatically broadcasts state changes or events to an arbitrary list of registered observers (subscribers) without knowing their concrete types.

### Structural Architecture
```text
┌──────────────────────────────────────┐
│           Subject (Feed)             │
├──────────────────────────────────────┤
│ - observers: List<Observer>          │
├──────────────────────────────────────┤
│ + subscribe(observer: Observer)      │
│ + unsubscribe(observer: Observer)    │
│ + notify(data: EventData)            │
└──────────────────▲───────────────────┘
                   │ broadcasts to
         ┌─────────┴─────────┐
         │                   │
┌────────┴────────┐ ┌────────┴────────┐
│ TradingStrategy │ │   RiskMonitor   │ (Observers)
└─────────────────┘ └─────────────────┘
```

### Multi-Language Implementations

#### Python
```python
from abc import ABC, abstractmethod
from typing import Any, Dict, List


class Observer(ABC):
    @abstractmethod
    def on_event(self, event_type: str, data: Dict[str, Any]) -> None:
        pass


class MarketFeed:
    def __init__(self) -> None:
        self._subscribers: List[Observer] = []

    def subscribe(self, observer: Observer) -> None:
        if observer not in self._subscribers:
            self._subscribers.append(observer)

    def unsubscribe(self, observer: Observer) -> None:
        self._subscribers.remove(observer)

    def emit(self, event_type: str, data: Dict[str, Any]) -> None:
        for sub in self._subscribers:
            sub.on_event(event_type, data)


class TradeDesk(Observer):
    def on_event(self, event_type: str, data: Dict[str, Any]) -> None:
        print(f"[Desk] Received {event_type}: {data}")


# Usage
feed = MarketFeed()
desk = TradeDesk()
feed.subscribe(desk)
feed.emit("PRICE_TICK", {"ticker": "NVDA", "price": 142.50})
```

#### Java (Thread-Safe Functional Interface + CopyOnWriteArrayList)
```java
import java.util.List;
import java.util.concurrent.CopyOnWriteArrayList;

@FunctionalInterface
public interface MarketObserver {
    void onTick(String symbol, double price);
}

public class MarketFeed {
    // Thread-safe list permitting safe concurrent iterations during event emission
    private final List<MarketObserver> listeners = new CopyOnWriteArrayList<>();

    public void subscribe(MarketObserver listener) {
        listeners.add(listener);
    }

    public void unsubscribe(MarketObserver listener) {
        listeners.remove(listener);
    }

    public void emit(String symbol, double price) {
        for (MarketObserver listener : listeners) {
            listener.onTick(symbol, price);
        }
    }
}

// Usage with Lambdas / Method References
MarketFeed feed = new MarketFeed();
feed.subscribe((sym, price) -> System.out.println("[Desk 1] " + sym + " traded at $" + price));
feed.subscribe((sym, price) -> System.out.println("[Risk Engine] Auditing tick for " + sym));

feed.emit("NVDA", 142.50);
```

#### C++
```cpp
#include <iostream>
#include <memory>
#include <string>
#include <vector>
#include <algorithm>

class Observer {
public:
    virtual ~Observer() = default;
    virtual void onEvent(const std::string& eventType, double value) = 0;
};

class MarketFeed {
public:
    void subscribe(std::shared_ptr<Observer> obs) {
        subscribers_.push_back(obs);
    }

    void emit(const std::string& eventType, double value) {
        for (auto& sub : subscribers_) {
            sub->onEvent(eventType, value);
        }
    }

private:
    std::vector<std::shared_ptr<Observer>> subscribers_;
};

class DisplayDashboard : public Observer {
public:
    void onEvent(const std::string& eventType, double value) override {
        std::cout << "[Dashboard] " << eventType << ": " << value << "\n";
    }
};
```

---

## 4. The Registry Pattern (Creational / Architectural)

### Core Concept & Intent
The **Registry Pattern** provides a centralized, decoupled catalog where components or plugins register themselves under unique keys. Callers instantiate or look up components dynamically without hardcoding `if/elif` ladders or switch statements.

It is heavily used in frameworks like **Spring** (bean registry), **PyTorch** (model registry), and **FastAPI** (router registry).

### Structural Architecture
```text
┌──────────────────────────────────────────────┐
│                   Registry                   │
├──────────────────────────────────────────────┤
│ - table: map<string, FactoryFunction>        │
├──────────────────────────────────────────────┤
│ + register(key: string, factory: Factory)    │
│ + create(key: string, ...args): Product      │
└───────────────────────▲──────────────────────┘
                        │ self-registers
        ┌───────────────┴───────────────┐
┌───────┴─────────┐           ┌─────────┴─────────┐
│  JsonProcessor  │           │   CsvProcessor    │
└─────────────────┘           └───────────────────┘
```

### Multi-Language Implementations

#### Python (Decorator-Driven Registry)
```python
from typing import Any, Callable, Dict, Type


class ParserRegistry:
    _catalog: Dict[str, Type["BaseParser"]] = {}

    @classmethod
    def register(cls, key: str) -> Callable[[Type["BaseParser"]], Type["BaseParser"]]:
        """Class decorator for self-registering parser subclasses."""
        def decorator(subclass: Type["BaseParser"]) -> Type["BaseParser"]:
            cls._catalog[key.lower()] = subclass
            return subclass

        return decorator

    @classmethod
    def create(cls, key: str, *args: Any, **kwargs: Any) -> "BaseParser":
        parser_cls = cls._catalog.get(key.lower())
        if not parser_cls:
            available = ", ".join(cls._catalog.keys())
            raise KeyError(f"Unknown parser: '{key}'. Available: [{available}]")
        return parser_cls(*args, **kwargs)


class BaseParser:
    def parse(self, text: str) -> str:
        raise NotImplementedError


@ParserRegistry.register("json")
class JsonParser(BaseParser):
    def parse(self, text: str) -> str:
        return f"Parsed JSON data: '{text}'"


@ParserRegistry.register("csv")
class CsvParser(BaseParser):
    def parse(self, text: str) -> str:
        return f"Parsed CSV rows: '{text}'"


# Dynamic factory instantiation
parser = ParserRegistry.create("json")
```

#### Java (Concurrent Map of Suppliers)
```java
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.function.Supplier;

public interface DocumentParser {
    String parse(String raw);
}

public class ParserRegistry {
    private static final Map<String, Supplier<DocumentParser>> REGISTRY = new ConcurrentHashMap<>();

    public static void register(String key, Supplier<DocumentParser> supplier) {
        REGISTRY.put(key.toLowerCase(), supplier);
    }

    public static DocumentParser create(String key) {
        Supplier<DocumentParser> supplier = REGISTRY.get(key.toLowerCase());
        if (supplier == null) {
            throw new IllegalArgumentException("Unknown parser: " + key);
        }
        return supplier.get();
    }
}

// Concrete implementation
public class JsonParser implements DocumentParser {
    @Override
    public String parse(String raw) { return "Parsed JSON: " + raw; }
}

// Self-registration via static initializer or application bootstrap
// ParserRegistry.register("json", JsonParser::new);
// DocumentParser parser = ParserRegistry.create("json");
```

#### C++ (Self-Registering Factory Map)
```cpp
#include <iostream>
#include <memory>
#include <string>
#include <unordered_map>
#include <functional>

class Parser {
public:
    virtual ~Parser() = default;
    virtual void parse(const std::string& input) = 0;
};

class ParserRegistry {
public:
    using FactoryFunc = std::function<std::unique_ptr<Parser>()>;

    static void registerParser(const std::string& key, FactoryFunc factory) {
        registry_[key] = std::move(factory);
    }

    static std::unique_ptr<Parser> create(const std::string& key) {
        auto it = registry_.find(key);
        if (it != registry_.end()) {
            return it->second();
        }
        return nullptr;
    }

private:
    static inline std::unordered_map<std::string, FactoryFunc> registry_;
};

class XmlParser : public Parser {
public:
    void parse(const std::string& input) override {
        std::cout << "Parsing XML: " << input << "\n";
    }
};

// Global static registration
static const bool xmlRegistered = []() {
    ParserRegistry::registerParser("xml", []() { return std::make_unique<XmlParser>(); });
    return true;
}();
```

---

## 5. The Factory Method Pattern (Creational)

### Core Concept & Intent
The **Factory Method Pattern** delegates object creation to specialized factory methods or subclasses without coupling client code to concrete classes.

### Multi-Language Implementations

#### Python
```python
from abc import ABC, abstractmethod


class PaymentProcessor(ABC):
    @abstractmethod
    def pay(self, amount: float) -> str:
        pass


class StripeProcessor(PaymentProcessor):
    def pay(self, amount: float) -> str:
        return f"Paid ${amount:.2f} via Stripe"


class PayPalProcessor(PaymentProcessor):
    def pay(self, amount: float) -> str:
        return f"Paid ${amount:.2f} via PayPal"


class PaymentFactory:
    @staticmethod
    def get_processor(method: str) -> PaymentProcessor:
        processors = {"stripe": StripeProcessor, "paypal": PayPalProcessor}
        cls = processors.get(method.lower())
        if not cls:
            raise ValueError(f"Unknown payment method: {method}")
        return cls()
```

#### Java (Polymorphic Interface + Pattern Matching Switch)
```java
public interface PaymentProcessor {
    String pay(double amount);
}

public class StripeProcessor implements PaymentProcessor {
    @Override
    public String pay(double amount) {
        return "Paid $" + amount + " via Stripe API";
    }
}

public class PayPalProcessor implements PaymentProcessor {
    @Override
    public String pay(double amount) {
        return "Paid $" + amount + " via PayPal Checkout";
    }
}

public class PaymentFactory {
    public static PaymentProcessor getProcessor(String type) {
        return switch (type.toLowerCase()) {
            case "stripe" -> new StripeProcessor();
            case "paypal" -> new PayPalProcessor();
            default -> throw new IllegalArgumentException("Unsupported payment type: " + type);
        };
    }
}
```

#### C++
```cpp
#include <iostream>
#include <memory>
#include <string>

class PaymentProcessor {
public:
    virtual ~PaymentProcessor() = default;
    virtual void pay(double amount) = 0;
};

class StripeProcessor : public PaymentProcessor {
public:
    void pay(double amount) override {
        std::cout << "Paid $" << amount << " via Stripe\n";
    }
};

class PaymentFactory {
public:
    static std::unique_ptr<PaymentProcessor> getProcessor(const std::string& type) {
        if (type == "stripe") return std::make_unique<StripeProcessor>();
        return nullptr;
    }
};
```

---

## 6. The Builder Pattern (Creational)

### Core Concept & Intent
The **Builder Pattern** constructs complex multi-attribute objects step-by-step through a fluent interface, avoiding bloated telescoping constructors.

### Multi-Language Implementations

#### Python
```python
from typing import List, Optional


class Query:
    def __init__(
        self,
        table: str,
        columns: List[str],
        filters: List[str],
        limit: Optional[int],
    ) -> None:
        self.table = table
        self.columns = columns
        self.filters = filters
        self.limit = limit

    def to_sql(self) -> str:
        cols = ", ".join(self.columns) if self.columns else "*"
        sql = f"SELECT {cols} FROM {self.table}"
        if self.filters:
            sql += f" WHERE {' AND '.join(self.filters)}"
        if self.limit is not None:
            sql += f" LIMIT {self.limit}"
        return f"{sql};"


class QueryBuilder:
    def __init__(self, table: str) -> None:
        self._table = table
        self._columns: List[str] = []
        self._filters: List[str] = []
        self._limit: Optional[int] = None

    def select(self, *columns: str) -> "QueryBuilder":
        self._columns.extend(columns)
        return self

    def where(self, condition: str) -> "QueryBuilder":
        self._filters.append(condition)
        return self

    def limit(self, count: int) -> "QueryBuilder":
        self._limit = count
        return self

    def build(self) -> Query:
        return Query(
            table=self._table,
            columns=self._columns,
            filters=self._filters,
            limit=self._limit,
        )


# Usage: Multi-line fluent method chaining
sql = (
    QueryBuilder("users")
    .select("id", "username", "email")
    .where("status = 'ACTIVE'")
    .where("created_at > '2026-01-01'")
    .limit(20)
    .build()
    .to_sql()
)
```

#### Java (Static Inner Builder - Effective Java)
```java
import java.util.List;

public class DatabaseQuery {
    private final String table;
    private final List<String> columns;
    private final Integer limit;

    private DatabaseQuery(Builder builder) {
        this.table = builder.table;
        this.columns = builder.columns;
        this.limit = builder.limit;
    }

    public String toSql() {
        String cols = (columns == null || columns.isEmpty()) ? "*" : String.join(", ", columns);
        String sql = "SELECT " + cols + " FROM " + table;
        if (limit != null) sql += " LIMIT " + limit;
        return sql + ";";
    }

    public static class Builder {
        private final String table;
        private List<String> columns;
        private Integer limit;

        public Builder(String table) { this.table = table; }

        public Builder select(String... cols) {
            this.columns = List.of(cols);
            return this;
        }

        public Builder limit(int limit) {
            this.limit = limit;
            return this;
        }

        public DatabaseQuery build() {
            return new DatabaseQuery(this);
        }
    }
}

// Usage
String sql = new DatabaseQuery.Builder("orders")
    .select("order_id", "total_amount")
    .limit(25)
    .build()
    .toSql();
```

#### C++
```cpp
#include <iostream>
#include <string>
#include <vector>

class HttpRequest {
public:
    std::string url;
    std::string method;
    int timeoutMs;
};

class HttpRequestBuilder {
public:
    explicit HttpRequestBuilder(std::string url) {
        request_.url = std::move(url);
        request_.method = "GET";
        request_.timeoutMs = 5000;
    }

    HttpRequestBuilder& setMethod(std::string method) {
        request_.method = std::move(method);
        return *this;
    }

    HttpRequestBuilder& setTimeout(int ms) {
        request_.timeoutMs = ms;
        return *this;
    }

    HttpRequest build() {
        return std::move(request_);
    }

private:
    HttpRequest request_;
};
```

---

## 7. The Adapter Pattern (Structural)

### Core Concept & Intent
The **Adapter Pattern** translates the interface of an existing, legacy, or third-party class into an expected target interface without modifying the original source code.

### Multi-Language Implementations

#### Python
```python
from abc import ABC, abstractmethod
import xml.etree.ElementTree as ET


class LegacyXmlService:
    """Adaptee: Third-party service returning raw XML."""
    def get_xml(self) -> str:
        return "<data><price>150.25</price></data>"


class PriceTarget(ABC):
    """Target interface expected by client code."""
    @abstractmethod
    def get_price(self) -> float:
        pass


class XmlPriceAdapter(PriceTarget):
    """Adapter bridging LegacyXmlService to PriceTarget."""
    def __init__(self, legacy: LegacyXmlService) -> None:
        self._legacy = legacy

    def get_price(self) -> float:
        root = ET.fromstring(self._legacy.get_xml())
        price_elem = root.find("price")
        if price_elem is None or price_elem.text is None:
            raise ValueError("Malformed XML: missing price tag")
        return float(price_elem.text)


# Usage
adapter = XmlPriceAdapter(LegacyXmlService())
print(f"Price via adapter: ${adapter.get_price():.2f}")
```

#### Java (Object Adapter Composition)
```java
// Adaptee: Legacy component with incompatible interface
public class LegacyFahrenheitSensor {
    public double readFahrenheit() {
        return 98.6;
    }
}

// Target interface expected by client code
public interface MetricTemperatureSensor {
    double getCelsius();
}

// Adapter bridging the two interfaces
public class TemperatureAdapter implements MetricTemperatureSensor {
    private final LegacyFahrenheitSensor legacySensor;

    public TemperatureAdapter(LegacyFahrenheitSensor legacySensor) {
        this.legacySensor = legacySensor;
    }

    @Override
    public double getCelsius() {
        return (legacySensor.readFahrenheit() - 32.0) * (5.0 / 9.0);
    }
}
```

#### C++
```cpp
#include <iostream>

class LegacySensor {
public:
    double readRawVolts() const { return 3.3; }
};

class MetricTarget {
public:
    virtual ~MetricTarget() = default;
    virtual double getPressureKPa() const = 0;
};

class SensorAdapter : public MetricTarget {
public:
    explicit SensorAdapter(const LegacySensor& legacy) : legacy_(legacy) {}

    double getPressureKPa() const override {
        return legacy_.readRawVolts() * 30.0; // Voltage to kPa translation
    }

private:
    const LegacySensor& legacy_;
};
```

---

## 8. The Decorator Pattern (Structural)

### Core Concept & Intent
The GoF **Decorator Pattern** wraps an existing object dynamically to layer on additional responsibilities without subclassing or modifying the underlying object.

### Multi-Language Implementations

#### Python
```python
from abc import ABC, abstractmethod


class DataSource(ABC):
    @abstractmethod
    def read(self) -> str:
        pass


class FileDataSource(DataSource):
    def read(self) -> str:
        return "CONFIDENTIAL_FINANCIAL_REPORT"


class EncryptionDecorator(DataSource):
    def __init__(self, source: DataSource) -> None:
        self._source = source

    def read(self) -> str:
        raw = self._source.read()
        return f"ENCRYPTED({raw})"
```

#### Java (Polymorphic Wrapping)
```java
public interface DataSource {
    String read();
}

public class FileDataSource implements DataSource {
    @Override
    public String read() {
        return "CONFIDENTIAL_FINANCIAL_REPORT";
    }
}

public abstract class DataSourceDecorator implements DataSource {
    protected final DataSource wrappee;

    public DataSourceDecorator(DataSource source) {
        this.wrappee = source;
    }

    @Override
    public String read() {
        return wrappee.read();
    }
}

public class EncryptionDecorator extends DataSourceDecorator {
    public EncryptionDecorator(DataSource source) { super(source); }

    @Override
    public String read() {
        return "ENCRYPTED(" + super.read() + ")";
    }
}

// Dynamic composition at runtime:
// DataSource secure = new EncryptionDecorator(new FileDataSource());
// System.out.println(secure.read());
```

#### C++
```cpp
#include <iostream>
#include <memory>
#include <string>

class Logger {
public:
    virtual ~Logger() = default;
    virtual void log(const std::string& msg) = 0;
};

class ConsoleLogger : public Logger {
public:
    void log(const std::string& msg) override {
        std::cout << "[LOG] " << msg << "\n";
    }
};

class TimestampDecorator : public Logger {
public:
    explicit TimestampDecorator(std::unique_ptr<Logger> logger) : logger_(std::move(logger)) {}

    void log(const std::string& msg) override {
        logger_->log("2026-09-26T11:00:00Z " + msg);
    }

private:
    std::unique_ptr<Logger> logger_;
};
```

---

## 9. The Strategy Pattern (Behavioral)

### Core Concept & Intent
The **Strategy Pattern** encapsulates a family of algorithms into interchangeable components, allowing client callers to swap algorithms at runtime without modifying client code.

### Multi-Language Implementations

#### Python
```python
from typing import Callable, List


# Strategies encapsulated as clean, testable callables
def vwap_execution_strategy(prices: List[float]) -> str:
    avg = sum(prices) / len(prices)
    return f"VWAP execution filled at avg price: ${avg:.2f}"


def limit_passive_strategy(prices: List[float]) -> str:
    best = min(prices)
    return f"Passive limit order placed at best bid: ${best:.2f}"


class OrderRouter:
    def __init__(self, strategy: Callable[[List[float]], str]) -> None:
        self.strategy = strategy

    def set_strategy(self, strategy: Callable[[List[float]], str]) -> None:
        self.strategy = strategy

    def route_order(self, book_depth: List[float]) -> str:
        return self.strategy(book_depth)


# Usage
depth = [142.10, 142.25, 142.50, 142.80]
router = OrderRouter(strategy=vwap_execution_strategy)
print(router.route_order(depth))

# Swap execution algorithm dynamically at runtime
router.set_strategy(limit_passive_strategy)
print(router.route_order(depth))
```

#### Java (Functional Interface & Method References)
```java
import java.util.List;

@FunctionalInterface
public interface PricingStrategy {
    double calculatePrice(double basePrice);
}

public class OrderContext {
    private PricingStrategy strategy;

    public OrderContext(PricingStrategy strategy) {
        this.strategy = strategy;
    }

    public void setStrategy(PricingStrategy strategy) {
        this.strategy = strategy;
    }

    public double getFinalPrice(double base) {
        return strategy.calculatePrice(base);
    }
}

// Usage with Lambdas:
PricingStrategy normal = price -> price;
PricingStrategy holidayDiscount = price -> price * 0.80;

OrderContext order = new OrderContext(normal);
System.out.println(order.getFinalPrice(100.0)); // 100.0

order.setStrategy(holidayDiscount);
System.out.println(order.getFinalPrice(100.0)); // 80.0
```

#### C++
```cpp
#include <iostream>
#include <functional>
#include <vector>

class RouteStrategy {
public:
    virtual ~RouteStrategy() = default;
    virtual void calculateRoute(const std::string& from, const std::string& to) = 0;
};

class FastRoute : public RouteStrategy {
public:
    void calculateRoute(const std::string& from, const std::string& to) override {
        std::cout << "Fastest highway route from " << from << " to " << to << "\n";
    }
};

class Navigator {
public:
    explicit Navigator(std::unique_ptr<RouteStrategy> strategy) : strategy_(std::move(strategy)) {}

    void navigate(const std::string& from, const std::string& to) {
        strategy_->calculateRoute(from, to);
    }

private:
    std::unique_ptr<RouteStrategy> strategy_;
};
```

---

## 10. The Chain of Responsibility Pattern (Behavioral)

### Core Concept & Intent
The **Chain of Responsibility Pattern** passes a request along a sequential pipeline of handlers. Each handler decides either to process the request, modify it, or forward it to the next link in the chain. It is the basis for HTTP middlewares across modern web frameworks.

### Multi-Language Implementations

#### Python
```python
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class Handler(ABC):
    def __init__(self) -> None:
        self._next: Optional["Handler"] = None

    def set_next(self, handler: "Handler") -> "Handler":
        self._next = handler
        return handler  # Enables fluent chaining: h1.set_next(h2).set_next(h3)

    @abstractmethod
    def handle(self, request: Dict[str, Any]) -> Optional[str]:
        if self._next is not None:
            return self._next.handle(request)
        return None


class AuthenticationHandler(Handler):
    def handle(self, request: Dict[str, Any]) -> Optional[str]:
        token = request.get("token")
        if token != "secret-token":
            return "401 Unauthorized: Invalid API Token"
        return super().handle(request)


class RoleValidationHandler(Handler):
    def handle(self, request: Dict[str, Any]) -> Optional[str]:
        role = request.get("role")
        if role != "ADMIN":
            return "403 Forbidden: Administrator role required"
        return super().handle(request)


# Usage
pipeline = AuthenticationHandler()
pipeline.set_next(RoleValidationHandler())

request = {"token": "secret-token", "role": "ADMIN"}
result = pipeline.handle(request)
print(f"Pipeline Result: {'SUCCESS' if result is None else result}")
```

#### Java (Middleware Pipeline)
```java
public abstract class Middleware {
    private Middleware next;

    public Middleware setNext(Middleware next) {
        this.next = next;
        return next;
    }

    public boolean check(String token, String role) {
        if (next != null) {
            return next.check(token, role);
        }
        return true;
    }
}

public class AuthenticationMiddleware extends Middleware {
    @Override
    public boolean check(String token, String role) {
        if (token == null || !token.equals("secret-token")) {
            System.out.println("401 Unauthorized: Invalid Token");
            return false;
        }
        return super.check(token, role);
    }
}

public class RoleMiddleware extends Middleware {
    @Override
    public boolean check(String token, String role) {
        if (!"ADMIN".equals(role)) {
            System.out.println("403 Forbidden: Insufficient Permissions");
            return false;
        }
        return super.check(token, role);
    }
}

// Chaining:
// Middleware chain = new AuthenticationMiddleware();
// chain.setNext(new RoleMiddleware());
// boolean allowed = chain.check("secret-token", "ADMIN");
```

#### C++
```cpp
#include <iostream>
#include <memory>
#include <string>

struct HttpRequest {
    std::string ip;
    bool isAuthenticated;
};

class MiddlewareHandler {
public:
    virtual ~MiddlewareHandler() = default;

    std::shared_ptr<MiddlewareHandler> setNext(std::shared_ptr<MiddlewareHandler> next) {
        next_ = next;
        return next;
    }

    virtual bool handle(const HttpRequest& req) {
        if (next_) return next_->handle(req);
        return true;
    }

private:
    std::shared_ptr<MiddlewareHandler> next_;
};

class AuthCheck : public MiddlewareHandler {
public:
    bool handle(const HttpRequest& req) override {
        if (!req.isAuthenticated) {
            std::cout << "Auth failed!\n";
            return false;
        }
        return MiddlewareHandler::handle(req);
    }
};
```

---

## Architectural Decision Matrix

```text
                        WHAT IS YOUR ARCHITECTURAL PROBLEM?
                                         │
         ┌───────────────────────────────┼───────────────────────────────┐
         ▼                               ▼                               ▼
 [OBJECT CREATION]               [STRUCTURE & MEMORY]            [BEHAVIOR & EVENTS]
         │                               │                               │
         ├─ Single global instance?      ├─ Millions of small objects?   ├─ 1-to-many event broadcast?
         │  ► SINGLETON                  │  ► FLYWEIGHT                  │  ► OBSERVER
         │                               │                               │
         ├─ Plugin/decorator catalog?    ├─ Incompatible interfaces?     ├─ Swap algorithm dynamically?
         │  ► REGISTRY                   │  ► ADAPTER                    │  ► STRATEGY
         │                               │                               │
         ├─ Complex step-by-step build?  ├─ Add dynamic features?        └─ Sequential request pipeline?
         │  ► BUILDER                    │  ► DECORATOR                     ► CHAIN OF RESPONSIBILITY
         │                               │
         └─ Abstract instantiation?      └─ Composition over inheritance
            ► FACTORY METHOD
```

---

## Conclusion

1. **In Python:** First-class functions, metaclasses, decorators, and `__slots__` replace heavy class scaffolding.
2. **In Java:** Strong static typing, `records`, functional interfaces, and concurrency primitives (`ConcurrentHashMap`, `CopyOnWriteArrayList`) provide robust, thread-safe enterprise implementations.
3. **In C++:** RAII, smart pointers (`std::unique_ptr`, `std::shared_ptr`), templates, and move semantics eliminate memory management hazards while maximizing execution performance.

Understanding how each language idiomatically models these patterns empowers you to design cleaner, maintainable, and high-performance software across any technology stack.
