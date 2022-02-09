import asyncio

from postman.models import (
    ApiItem,
    Endpoint,
    QueryParam,
    Role,
    Tag,
    User,
    init_db,
)
from postman.models.mixins import destroy_db


async def create_roles():
    await Role.create(
        name="superuser", level=0, description="Can do everything"
    )


async def create_users():
    superuser = await Role.get(name="superuser")
    await User.create(
        first_name="Slim",
        last_name="Beji",
        email="mslimbeji@gmail.com",
        password="secret",
        active=True,
        role=superuser,
    )


async def create_tags():
    tags = [
        "carbon",
        "ecology",
        "blockchain",
        "cryptocurrency",
        "bitcoin",
        "currency",
        "football",
        "stats",
        "weather",
    ]
    for text in tags:
        await Tag.create(text=text)


async def create_apis():
    apis = [
        {
            "label": "Carbon Intensity API",
            "description": "A carbon intensity forecast API",
            "url": "https://api.carbonintensity.org.uk",
            "tags": ["carbon", "ecology"],
            "endpoints": [
                {
                    "url": "/generation",
                    "label": "Generation",
                    "description": "Carbon Generation",
                    "http_method": "get",
                    "tags": ["carbon", "ecology"],
                    "query_params": [],
                },
                {
                    "url": "/intensity/date",
                    "label": "Intensity",
                    "description": "Carbon intensity by date",
                    "http_method": "get",
                    "tags": ["carbon", "ecology"],
                    "query_params": [],
                },
                {
                    "url": "/intensity/factors",
                    "label": "Factors",
                    "description": "Factors of carbon intensity",
                    "http_method": "get",
                    "tags": ["carbon", "ecology"],
                    "query_params": [],
                },
            ],
        },
        {
            "label": "CoinGecko",
            "description": "CoinGecko cryptocurrencies api",
            "url": "https://api.coingecko.com/api/v3",
            "tags": ["blockchain", "cryptocurrency", "bitcoin", "currency"],
            "endpoints": [
                {
                    "url": "/coins/list",
                    "label": "Coins list",
                    "description": "List the cryptocurrencies supported by CoinGecko",
                    "http_method": "get",
                    "tags": ["blockchain", "cryptocurrency"],
                    "query_params": [],
                },
                {
                    "url": "/coins/markets",
                    "label": "Market state",
                    "description": "Market State of Cryptocurrencies",
                    "http_method": "get",
                    "tags": ["blockchain", "cryptocurrency", "currency"],
                    "query_params": [
                        {
                            "type": "string",
                            "description": "currency reference (Example: usd, eur ...)",
                            "default": "usd",
                            "required": True,
                            "location": "query",
                            "label": "vs_currency",
                        },
                    ],
                },
                {
                    "url": "/coins/bitcoin/history",
                    "label": "Bitcoin Snapshot",
                    "description": "A Bitcoin State Snapshot",
                    "http_method": "get",
                    "tags": ["bitcoin", "cryptocurrency"],
                    "query_params": [
                        {
                            "type": "string",
                            "description": "Date",
                            "default": "30-08-2020",
                            "required": True,
                            "location": "query",
                            "label": "date",
                        },
                    ],
                },
                {
                    "url": "/bitcoin/market_chart",
                    "label": "Bitcoin Market Chart",
                    "description": "Bitcoin Time Evolution",
                    "http_method": "get",
                    "tags": ["bitcoin", "cryptocurrency"],
                    "query_params": [
                        {
                            "type": "integer",
                            "description": "Number of days",
                            "default": "100",
                            "required": True,
                            "location": "query",
                            "label": "days",
                        },
                        {
                            "type": "string",
                            "description": "currency reference (Example: usd, eur ...)",
                            "default": "usd",
                            "required": True,
                            "location": "query",
                            "label": "vs_currency",
                        },
                    ],
                },
            ],
        },
        {
            "label": "Currencies rates",
            "description": "Currency exchange rates API",
            "url": "https://api.exchangeratesapi.io",
            "tags": ["currency"],
            "endpoints": [
                {
                    "url": "/latest",
                    "label": "exchange rates",
                    "description": "Get Latest exchange rates",
                    "http_method": "get",
                    "tags": ["currency"],
                    "query_params": [
                        {
                            "type": "string",
                            "description": "The base currency for exchange rates",
                            "default": "EUR",
                            "required": False,
                            "location": "query",
                            "label": "base",
                        },
                        {
                            "type": "string",
                            "description": "A restricted list of currencies comma separetd (Ex: USD,GBP)",
                            "default": None,
                            "required": False,
                            "location": "query",
                            "label": "symbols",
                        },
                    ],
                },
                {
                    "url": "/history",
                    "label": "Currencies historical rates",
                    "description": "Get historical exchange rates evolutions",
                    "http_method": "get",
                    "tags": ["currency"],
                    "query_params": [
                        {
                            "type": "start date",
                            "description": "The base currency for exchange rates",
                            "default": "2018-09-01",
                            "required": True,
                            "location": "query",
                            "label": "start_at",
                        },
                        {
                            "type": "string",
                            "description": "end_date",
                            "default": "2018-09-01",
                            "required": True,
                            "location": "query",
                            "label": "end_at",
                        },
                        {
                            "type": "string",
                            "description": "The base currency for exchange rates",
                            "default": "EUR",
                            "required": False,
                            "location": "query",
                            "label": "base",
                        },
                        {
                            "type": "string",
                            "description": "A restricted list of currencies comma separetd (Ex: USD,GBP)",
                            "default": None,
                            "required": False,
                            "location": "query",
                            "label": "symbols",
                        },
                    ],
                },
            ],
        },
        {
            "label": "Football-data",
            "description": "Football Stats API",
            "url": "http://api.football-data.org/v2",
            "tags": ["football", "stats"],
            "endpoints": [
                {
                    "url": "/competitions/2021/teams",
                    "label": "Premier League Teams",
                    "description": "List of the premier league teams per season",
                    "http_method": "get",
                    "tags": ["football"],
                    "query_params": [
                        {
                            "type": "integer",
                            "description": "Season start",
                            "default": 2020,
                            "required": True,
                            "location": "query",
                            "label": "season",
                        },
                        {
                            "type": "string",
                            "description": "The access token",
                            "default": "4138c69d99c1436a81e60f812530290d",
                            "required": True,
                            "location": "header",
                            "label": "X-Auth-Token",
                        },
                    ],
                },
                {
                    "url": "/competitions/2021/standings",
                    "label": "Standings",
                    "description": "Get Premier League standing",
                    "http_method": "get",
                    "tags": ["football", "stats"],
                    "query_params": [
                        {
                            "type": "integer",
                            "description": "Season start",
                            "default": 2020,
                            "required": True,
                            "location": "query",
                            "label": "season",
                        },
                        {
                            "type": "string",
                            "description": "The access token",
                            "default": "4138c69d99c1436a81e60f812530290d",
                            "required": True,
                            "location": "header",
                            "label": "X-Auth-Token",
                        },
                    ],
                },
                {
                    "url": "/competitions/2021/matches",
                    "label": "Fixtures",
                    "description": "Get Premier League Matches",
                    "http_method": "get",
                    "tags": ["football"],
                    "query_params": [
                        {
                            "type": "integer",
                            "description": "Season start",
                            "default": 2020,
                            "required": True,
                            "location": "query",
                            "label": "season",
                        },
                        {
                            "type": "string",
                            "description": "The access token",
                            "default": "4138c69d99c1436a81e60f812530290d",
                            "required": True,
                            "location": "header",
                            "label": "X-Auth-Token",
                        },
                        {
                            "type": "integer",
                            "description": "The fixture",
                            "default": None,
                            "required": False,
                            "location": "query",
                            "label": "matchday",
                        },
                        {
                            "type": "string",
                            "description": "Starting Date Filter",
                            "default": "2019-10-12",
                            "required": False,
                            "location": "query",
                            "label": "dateFrom",
                        },
                        {
                            "type": "string",
                            "description": "End Date Filter",
                            "default": "2019-11-12",
                            "required": False,
                            "location": "query",
                            "label": "dateTo",
                        },
                    ],
                },
                {
                    "url": "/competitions/2021/scorers",
                    "label": "Scorers",
                    "description": "Premier League scorers stats",
                    "http_method": "get",
                    "tags": ["football", "stats"],
                    "query_params": [
                        {
                            "type": "integer",
                            "description": "Season start",
                            "default": 2020,
                            "required": True,
                            "location": "query",
                            "label": "season",
                        },
                        {
                            "type": "string",
                            "description": "The access token",
                            "default": "4138c69d99c1436a81e60f812530290d",
                            "required": True,
                            "location": "header",
                            "label": "X-Auth-Token",
                        },
                    ],
                },
            ],
        },
        {
            "label": "Weather API",
            "description": "A Weather API",
            "url": "https://api.openweathermap.org",
            "tags": ["weather"],
            "endpoints": [
                {
                    "url": "/data/2.5/weather",
                    "label": "Current Weather",
                    "description": "Get the current weather",
                    "http_method": "get",
                    "tags": ["weather"],
                    "query_params": [
                        {
                            "type": "string",
                            "description": "The API Key",
                            "default": "a7c2ae8e758abfb3756b74a6ef237f83",
                            "required": True,
                            "location": "query",
                            "label": "appid",
                        },
                        {
                            "type": "string",
                            "description": "Geo-localisation query (Example: paris,london)",
                            "default": "paris",
                            "required": False,
                            "location": "query",
                            "label": "q",
                        },
                        {
                            "type": "float",
                            "description": "Lattitude",
                            "default": 33.8869,
                            "required": False,
                            "location": "query",
                            "label": "lat",
                        },
                        {
                            "type": "float",
                            "description": "Longitude",
                            "default": 9.5375,
                            "required": False,
                            "location": "query",
                            "label": "lon",
                        },
                    ],
                },
                {
                    "url": "/data/2.5/forecast",
                    "label": "Weather Forecast",
                    "description": "Get a weather Forecast",
                    "http_method": "get",
                    "tags": ["weather"],
                    "query_params": [
                        {
                            "type": "string",
                            "description": "The API Key",
                            "default": "a7c2ae8e758abfb3756b74a6ef237f83",
                            "required": True,
                            "location": "query",
                            "label": "appid",
                        },
                        {
                            "type": "string",
                            "description": "Geo-localisation query (Example: paris,london)",
                            "default": "paris",
                            "required": False,
                            "location": "query",
                            "label": "q",
                        },
                        {
                            "type": "integer",
                            "description": "Number of days for forecast",
                            "default": 2,
                            "required": False,
                            "location": "query",
                            "label": "cnt",
                        },
                    ],
                },
            ],
        },
    ]
    for data in apis:
        tags = data.pop("tags")
        endpoints = data.pop("endpoints")
        api_item = await ApiItem.create(**data)

        tag_instnaces = []
        for tag in tags:
            tag_instance = await Tag.get(text=tag)
            tag_instnaces.append(tag_instance)
        await api_item.tags.add(*tag_instnaces)

        for endpoint_data in endpoints:
            endpoint_tags = endpoint_data.pop("tags")
            query_params = endpoint_data.pop("query_params")
            endpoint_item = await Endpoint.create(
                **endpoint_data, api_item=api_item
            )

            endpoint_tag_instnaces = []
            for tag in endpoint_tags:
                tag_instance = await Tag.get(text=tag)
                endpoint_tag_instnaces.append(tag_instance)
            await endpoint_item.tags.add(*endpoint_tag_instnaces)

            for query_param_data in query_params:
                await QueryParam.create(
                    **query_param_data, endpoint=endpoint_item
                )


async def seed_db():
    await destroy_db()
    await init_db()
    await create_roles()
    await create_users()
    await create_tags()
    await create_apis()


asyncio.run(seed_db())
