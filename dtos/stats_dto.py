from pydantic import BaseModel, Field


class TokenUsageDTO(BaseModel):
    recent: int
    recent_input: int
    recent_output: int
    total: int
    total_input: int
    total_output: int


class EnergyUsageDTO(BaseModel):
    recent_wh: float
    total_wh: float
    per_message_wh: float
    equivalent: str


class ThinkingTimeDTO(BaseModel):
    average: float
    total: float


class ModelUsageStatsDTO(BaseModel):
    count: int
    input_tokens: int
    output_tokens: int


class UserStatsDTO(BaseModel):
    total_chats: int
    recent_chats: int
    total_messages: int
    avg_messages_per_chat: float
    messages_per_day: dict[str, int]
    chats_per_day: dict[str, int]
    token_usage: TokenUsageDTO
    energy_usage: EnergyUsageDTO
    thinking_time: ThinkingTimeDTO
    efficiency: int
    model_usage: dict[str, ModelUsageStatsDTO]


class DailyStatsDTO(BaseModel):
    date: str
    conversations: int
    messages: int


class WeeklyConversationStatsDTO(BaseModel):
    total_conversations: int
    total_messages: int
    daily_breakdown: list[DailyStatsDTO]


class MessageDistributionDTO(BaseModel):
    by_role: dict[str, int]
    by_model: dict[str, int]
    total_messages: int


class UsagePeriodDTO(BaseModel):
    days: int
    start_date: str
    end_date: str


class TopProviderDTO(BaseModel):
    name: str
    chats: int
    rank: int


class UsageSummaryDTO(BaseModel):
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
    top_providers: list[TopProviderDTO]


class ChatStatisticsDTO(BaseModel):
    total_chats: int
    avg_messages_per_chat: float
    longest_chat: dict | None
    chat_distribution_by_provider: dict[str, int]
    recent_chats: list[dict]


class ModelBreakdownDTO(BaseModel):
    messages: int
    input_tokens: int
    output_tokens: int
    cost: float


class ProviderBreakdownDTO(BaseModel):
    messages: int
    chats: int
    input_tokens: int
    output_tokens: int
    cost: float
    avg_messages_per_chat: float


class UsageOverviewDTO(BaseModel):
    period: UsagePeriodDTO
    summary: UsageSummaryDTO
    model_breakdown: dict[str, ModelBreakdownDTO]
    provider_breakdown: dict[str, ProviderBreakdownDTO]
    chat_statistics: ChatStatisticsDTO


class TimelineDataPointDTO(BaseModel):
    timestamp: str
    messages: int
    chats: int
    input_tokens: int
    output_tokens: int
    total_tokens: int
    cost_usd: float
    energy_wh: float


class UsageTimelineDTO(BaseModel):
    granularity: str
    period: UsagePeriodDTO
    timeline: list[TimelineDataPointDTO]


class UsagePatternsDTO(BaseModel):
    period: UsagePeriodDTO
    hourly_distribution: dict[str, int]
    daily_distribution: dict[str, int]
    peak_hour: str
    peak_day: str
