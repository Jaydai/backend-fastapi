from dataclasses import dataclass


@dataclass
class TokenUsage:
    recent: int
    recent_input: int
    recent_output: int
    total: int
    total_input: int
    total_output: int


@dataclass
class EnergyUsage:
    recent_wh: float
    total_wh: float
    per_message_wh: float
    equivalent: str


@dataclass
class ThinkingTime:
    average: float
    total: float


@dataclass
class ModelUsageStats:
    count: int
    input_tokens: int
    output_tokens: int


@dataclass
class UserStats:
    total_chats: int
    recent_chats: int
    total_messages: int
    avg_messages_per_chat: float
    messages_per_day: dict[str, int]
    chats_per_day: dict[str, int]
    token_usage: TokenUsage
    energy_usage: EnergyUsage
    thinking_time: ThinkingTime
    efficiency: int
    model_usage: dict[str, ModelUsageStats]


@dataclass
class DailyStats:
    date: str
    conversations: int
    messages: int


@dataclass
class WeeklyConversationStats:
    total_conversations: int
    total_messages: int
    daily_breakdown: list[DailyStats]


@dataclass
class MessageDistribution:
    by_role: dict[str, int]
    by_model: dict[str, int]
    total_messages: int


@dataclass
class UsagePeriod:
    days: int
    start_date: str
    end_date: str


@dataclass
class UsageSummary:
    total_messages: int
    total_chats: int
    total_tokens: int
    input_tokens: int
    output_tokens: int
    estimated_cost_usd: float
    energy_consumption_wh: float
    co2_emissions_kg: float
    avg_messages_per_chat: float
    most_used_provider: str | None
    top_providers: list[dict]


@dataclass
class ChatStatistics:
    total_chats: int
    avg_messages_per_chat: float
    longest_chat: dict | None
    chat_distribution_by_provider: dict[str, int]
    recent_chats: list[dict]


@dataclass
class UsageOverview:
    period: UsagePeriod
    summary: UsageSummary
    model_breakdown: dict
    provider_breakdown: dict
    chat_statistics: ChatStatistics


@dataclass
class TimelineDataPoint:
    timestamp: str
    messages: int
    chats: int
    input_tokens: int
    output_tokens: int
    total_tokens: int
    cost_usd: float
    energy_wh: float


@dataclass
class UsageTimeline:
    granularity: str
    period: UsagePeriod
    timeline: list[TimelineDataPoint]


@dataclass
class UsagePatterns:
    period: UsagePeriod
    hourly_distribution: dict[str, int]
    daily_distribution: dict[str, int]
    peak_hour: str
    peak_day: str
