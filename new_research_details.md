# 🔴 CRITICAL: MANDATORY TOOL USAGE to perform all task(s) - NEVER stop using tools - continue using them until tasks completion

🔴 CRITICAL: You MUST use ALL available tools AS OFTEN AS NEEDED throughout the entire task execution. This is NOT a one-time checklist - you must continuously use tools throughout the process

🔴 REMEMBER: The tool list is your toolkit - use every tool as often as needed, in any order, throughout the entire task execution. Choose the right tool for the right operation

TOOL USAGE REQUIREMENTS:

- Use tools in ANY ORDER as needed for the specific task
- Use the SAME tool MULTIPLE TIMES if needed
- NEVER treat tool lists as a rigid sequence
- ALWAYS use tools when they would be helpful, even if you've used them before
- Use tools for investigation, analysis, verification, and implementation at every step

MANDATORY TOOL USAGE PATTERNS:

1. START with Sequential-Thinking for task analysis, Investigation, Planning, Scoping, Researching, Complex problem analysis (max 8 thoughts)
2. Use Serena Tools for code analysis, symbol manipulation, pattern search with context, and memory management for complex financial algorithm development and refactoring; Use standard Read/Write/Edit for simple file content modifications
3. REPEAT any tool as needed throughout the process
4. 🔴 NEVER stop using tools - continue using them until task completion

VIOLATION PENALTIES:

- If you use tools only once and stop, you're failing
- If you follow a rigid order instead of using tools as needed, you're failing
- If you don't use tools throughout the entire process, you're failingplan

SUCCESS CRITERIA:

- Tools used multiple times throughout the task
- Tools used in different orders based on need
- Continuous tool usage from start to finish
- Correct tool selection based on operation type
- No rigid sequencing - only logical tool usage based on task requirements

🔴 REMEMBER: The tool list is your toolkit - use every tool as often as needed, in any order, throughout the entire task execution. Choose the right tool for the right operation

---

<Research Topic Details> 🔴 CRITICAL: DO NOT START ANY IMPLEMENTATION DURING THIS PHASE 🔴

1. Create new AI Agent Tool 'get_call_options_chain' that will use the Polygon.io Direct API using the 'list_snapshot_options_chain' endpoint to retrieve the Call Options Chain with 10 Strike Prices above the current underlying price.  AI Agent instructions also need to be updated on how to use the new tool(s)
- Round Up\Down to 2 decimal points Max for final response
- AI Agent Requires these inputs for a proper tool call: <Ticker>, <Ticker's Current Price>, <Expiration Date>
- Once those 3x inputs are known, then the tool call inputs params for the Polygon 'list_snapshot_options_chain' endpoint will be:

"
For new Call Options Chain tool 'get_call_options_chain':
<Ticker>
"strike_price.gte": <Ticker's Current Price>,
"expiration_date": <Expiration Date>,
"contract_type": "call", // This will be HARDCODED for CALL Options Chain
"order": "asc", // This will be HARDCODED for CALL Options Chain
"limit": 10, // This will be HARDCODED for ALL Options Chain
"sort": "strike_price", // This will be HARDCODED for ALL Options Chain
"

Response Formatting for Call Options Chain needs to be in this format for the example query of "Fetch SPY Call Options Chain Expiration Date 10/10/25", where SPY is currently ~$673:

"SPY Call Options Chain: 2025-10-10": {
    "$673": {
        "close": $2.28,
        "delta": 0.51,
        "gamma": 0.07,
        "theta": -0.63,
        "implied_volatility": 0.11,
        "volume": 18777,
        "open_interest": 6420
    }
    "$674": {
        "close": $1.68,
        "delta": 0.44,
        "gamma": 0.08,
        "theta": -0.57,
        "implied_volatility": 0.11,
        "volume": 10405,
        "open_interest": 7866
    }
    "$675": {
        "close": $1.16,
        "delta": 0.36,
        "gamma": 0.08,
        "theta": -0.52,
        "implied_volatility": 0.10,
        "volume": 25727,
        "open_interest": 16166
    }
...
}


Here is the example Polygon Endpoint Call for the Call Options Chain: 

"
from polygon import RESTClient

client = RESTClient("8VH7tsIYkBruV6ipSUoI_Cy8Onp2yl7v")

options_chain = []
for o in client.list_snapshot_options_chain(
    "SPY",
    params={
        "strike_price.gte": 673,
        "expiration_date": "2025-10-10",
        "contract_type": "call",
        "order": "asc",
        "limit": 10,
        "sort": "strike_price",
    },
):
    options_chain.append(o)

print(options_chain)
"

Here is the example Polygon Endpoint Call full response that is UNFORMATTED.  So AI Agent will need to re-format and ONLY respond with the requested output formatting previously specified.  The full options chain is very verbose with alot of not needed details, so the formated response strips out and only shows the essential info.

"
{
  "results": [
    {
      "day": {
        "change": 0.87,
        "change_percent": 61.702,
        "close": 2.28,
        "high": 2.39,
        "last_updated": 1759896000000000000,
        "low": 1.18,
        "open": 1.41,
        "previous_close": 1.41,
        "volume": 18777,
        "vwap": 2.0417
      },
      "details": {
        "contract_type": "call",
        "exercise_style": "american",
        "expiration_date": "2025-10-10",
        "shares_per_contract": 100,
        "strike_price": 673,
        "ticker": "O:SPY251010C00673000"
      },
      "greeks": {
        "delta": 0.5163667483288759,
        "gamma": 0.0743331452230593,
        "theta": -0.6350250427982884,
        "vega": 0.18871522554021333
      },
      "implied_volatility": 0.11484577671143054,
      "open_interest": 6420,
      "underlying_asset": {
        "ticker": "SPY"
      }
    },
    {
      "day": {
        "change": 0.65,
        "change_percent": 63.107,
        "close": 1.68,
        "high": 1.79,
        "last_updated": 1759896000000000000,
        "low": 0.85,
        "open": 1.04,
        "previous_close": 1.03,
        "volume": 10405,
        "vwap": 1.437
      },
      "details": {
        "contract_type": "call",
        "exercise_style": "american",
        "expiration_date": "2025-10-10",
        "shares_per_contract": 100,
        "strike_price": 674,
        "ticker": "O:SPY251010C00674000"
      },
      "greeks": {
        "delta": 0.4393436629465123,
        "gamma": 0.07832593206441349,
        "theta": -0.5723301928378498,
        "vega": 0.18953651594268955
      },
      "implied_volatility": 0.10634052787900895,
      "open_interest": 7866,
      "underlying_asset": {
        "ticker": "SPY"
      }
    },
    {
      "day": {
        "change": 0.4,
        "change_percent": 52.632,
        "close": 1.16,
        "high": 1.28,
        "last_updated": 1759896000000000000,
        "low": 0.59,
        "open": 0.75,
        "previous_close": 0.76,
        "volume": 25727,
        "vwap": 1.0295
      },
      "details": {
        "contract_type": "call",
        "exercise_style": "american",
        "expiration_date": "2025-10-10",
        "shares_per_contract": 100,
        "strike_price": 675,
        "ticker": "O:SPY251010C00675000"
      },
      "greeks": {
        "delta": 0.3559503489458921,
        "gamma": 0.07835681986429108,
        "theta": -0.5221115493619091,
        "vega": 0.1666856413410707
      },
      "implied_volatility": 0.10177923924941987,
      "open_interest": 16166,
      "underlying_asset": {
        "ticker": "SPY"
      }
    },
    {
      "day": {
        "change": 0.23,
        "change_percent": 42.593,
        "close": 0.77,
        "high": 0.87,
        "last_updated": 1759896000000000000,
        "low": 0.4,
        "open": 0.51,
        "previous_close": 0.54,
        "volume": 7722,
        "vwap": 0.7029
      },
      "details": {
        "contract_type": "call",
        "exercise_style": "american",
        "expiration_date": "2025-10-10",
        "shares_per_contract": 100,
        "strike_price": 676,
        "ticker": "O:SPY251010C00676000"
      },
      "greeks": {
        "delta": 0.27183367020910654,
        "gamma": 0.07311786643530027,
        "theta": -0.43207684946721553,
        "vega": 0.1677196134691216
      },
      "implied_volatility": 0.09598139617534633,
      "open_interest": 4387,
      "underlying_asset": {
        "ticker": "SPY"
      }
    },
    {
      "day": {
        "change": 0.12,
        "change_percent": 33.333,
        "close": 0.48,
        "high": 0.57,
        "last_updated": 1759896000000000000,
        "low": 0.26,
        "open": 0.34,
        "previous_close": 0.36,
        "volume": 9911,
        "vwap": 0.4491
      },
      "details": {
        "contract_type": "call",
        "exercise_style": "american",
        "expiration_date": "2025-10-10",
        "shares_per_contract": 100,
        "strike_price": 677,
        "ticker": "O:SPY251010C00677000"
      },
      "greeks": {
        "delta": 0.19610846493685538,
        "gamma": 0.06323431249441634,
        "theta": -0.34464262884953273,
        "vega": 0.1291130312728323
      },
      "implied_volatility": 0.09232427425945954,
      "open_interest": 5230,
      "underlying_asset": {
        "ticker": "SPY"
      }
    },
    {
      "day": {
        "change": 0.06,
        "change_percent": 26.087,
        "close": 0.29,
        "high": 0.35,
        "last_updated": 1759896000000000000,
        "low": 0.17,
        "open": 0.21,
        "previous_close": 0.23,
        "volume": 7543,
        "vwap": 0.2674
      },
      "details": {
        "contract_type": "call",
        "exercise_style": "american",
        "expiration_date": "2025-10-10",
        "shares_per_contract": 100,
        "strike_price": 678,
        "ticker": "O:SPY251010C00678000"
      },
      "greeks": {
        "delta": 0.1326791805442094,
        "gamma": 0.05038123662157967,
        "theta": -0.2647495169337782,
        "vega": 0.08662757513603726
      },
      "implied_volatility": 0.09081748249189588,
      "open_interest": 6378,
      "underlying_asset": {
        "ticker": "SPY"
      }
    },
    {
      "day": {
        "change": 0.01,
        "change_percent": 6.667,
        "close": 0.16,
        "high": 0.21,
        "last_updated": 1759896000000000000,
        "low": 0.11,
        "open": 0.15,
        "previous_close": 0.15,
        "volume": 3814,
        "vwap": 0.1658
      },
      "details": {
        "contract_type": "call",
        "exercise_style": "american",
        "expiration_date": "2025-10-10",
        "shares_per_contract": 100,
        "strike_price": 679,
        "ticker": "O:SPY251010C00679000"
      },
      "greeks": {
        "delta": 0.08421656667729469,
        "gamma": 0.03688207700318067,
        "theta": -0.18306846813023092,
        "vega": 0.08727393585646605
      },
      "implied_volatility": 0.08835999822923733,
      "open_interest": 3694,
      "underlying_asset": {
        "ticker": "SPY"
      }
    },
    {
      "day": {
        "change": -0.02,
        "change_percent": -20,
        "close": 0.08,
        "high": 0.13,
        "last_updated": 1759896000000000000,
        "low": 0.06,
        "open": 0.1,
        "previous_close": 0.1,
        "volume": 10964,
        "vwap": 0.09
      },
      "details": {
        "contract_type": "call",
        "exercise_style": "american",
        "expiration_date": "2025-10-10",
        "shares_per_contract": 100,
        "strike_price": 680,
        "ticker": "O:SPY251010C00680000"
      },
      "greeks": {
        "delta": 0.048777607306760944,
        "gamma": 0.024675125846168947,
        "theta": -0.11527661734563618,
        "vega": 0.05094482014071309
      },
      "implied_volatility": 0.08580625025768449,
      "open_interest": 12337,
      "underlying_asset": {
        "ticker": "SPY"
      }
    },
    {
      "day": {
        "change": -0.01,
        "change_percent": -16.7,
        "close": 0.05,
        "high": 0.08,
        "last_updated": 1759896000000000000,
        "low": 0.03,
        "open": 0.06,
        "previous_close": 0.06,
        "volume": 1847,
        "vwap": 0.05988
      },
      "details": {
        "contract_type": "call",
        "exercise_style": "american",
        "expiration_date": "2025-10-10",
        "shares_per_contract": 100,
        "strike_price": 681,
        "ticker": "O:SPY251010C00681000"
      },
      "greeks": {
        "delta": 0.028064990735975466,
        "gamma": 0.01574793214489857,
        "theta": -0.0738777025049129,
        "vega": 0.025627618813827184
      },
      "implied_volatility": 0.08608296443389207,
      "open_interest": 6346,
      "underlying_asset": {
        "ticker": "SPY"
      }
    },
    {
      "day": {
        "change": -0.03,
        "change_percent": -60,
        "close": 0.02,
        "high": 0.05,
        "last_updated": 1759896000000000000,
        "low": 0.02,
        "open": 0.03,
        "previous_close": 0.05,
        "volume": 3491,
        "vwap": 0.03712
      },
      "details": {
        "contract_type": "call",
        "exercise_style": "american",
        "expiration_date": "2025-10-10",
        "shares_per_contract": 100,
        "strike_price": 682,
        "ticker": "O:SPY251010C00682000"
      },
      "greeks": {
        "delta": 0.016371043405782475,
        "gamma": 0.00980234018227309,
        "theta": -0.04692213275023003,
        "vega": 0.02576232992049706
      },
      "implied_volatility": 0.08702620329455144,
      "open_interest": 8339,
      "underlying_asset": {
        "ticker": "SPY"
      }
    }
  ],
  "status": "OK",
  "request_id": "027662f8fe3f6ee5199c613a24511262",
  "next_url": "https://api.polygon.io/v3/snapshot/options/SPY?cursor=YXA9TyUzQVNQWTI1MTAxMEMwMDY4MjAwMCZhcz0mY29udHJhY3RfdHlwZT1jYWxsJmV4cGlyYXRpb25fZGF0ZT0yMDI1LTEwLTEwJmxpbWl0PTEwJm9yZGVyPWFzYyZzb3J0PXN0cmlrZV9wcmljZSZzdHJpa2VfcHJpY2UuZ3RlPTY4Mi4wMDAwMDA"
}
"

2. Create new AI Agent Tool 'get_put_options_chain' that will use the Polygon.io Direct API using the 'list_snapshot_options_chain' endpoint to retrieve the Put Options Chain with 10 Strike Prices below the current underlying price. AI Agent instructions also need to be updated on how to use the new tool(s)
- Round Up\Down to 2 decimal points Max for final response
- AI Agent Requires these inputs for a proper tool call: <Ticker>, <Ticker's Current Price>, <Expiration Date>
- Once those 3x inputs are known, then the tool call inputs params for the Polygon 'list_snapshot_options_chain' endpoint will be:

"
For new Put Options Chain tool 'get_put_options_chain':
<Ticker>
"strike_price.lte": <Ticker's Current Price>,
"expiration_date": <Expiration Date>,
"contract_type": "put", // This will be HARDCODED for PUT Options Chain
"order": "desc", // This will be HARDCODED for PUT Options Chain
"limit": 10, // This will be HARDCODED for ALL Options Chain
"sort": "strike_price", // This will be HARDCODED for ALL Options Chain
"

Response Formatting for Put Options Chain needs to be in this format for the example query of "Fetch Put Call Options Chain Expiration Date 10/10/25", where SPY is currently ~$673:

"SPY Put Options Chain: 2025-10-10" : {
    "$673": {
        "close": $1.68,
        "delta": -0.48,
        "gamma": 0.09,
        "theta": -0.47,
        "implied_volatility": 0.09,
        "volume": 22280,
        "open_interest": 3139
    }
    "$672": {
        "close": $1.37,
        "delta": 0.40,
        "gamma": 0.08,
        "theta": -0.48,
        "implied_volatility": 0.10,
        "volume": 42831,
        "open_interest": 6509
    }
    "$671": {
        "close": $1.13,
        "delta": 0.33,
        "gamma": 0.07,
        "theta": -0.50,
        "implied_volatility": 0.11,
        "volume": 21707,
        "open_interest": 10084
    }
...
}


Here is the example Polygon Endpoint Call for the Put Options Chain: 

"
from polygon import RESTClient

client = RESTClient("8VH7tsIYkBruV6ipSUoI_Cy8Onp2yl7v")

options_chain = []
for o in client.list_snapshot_options_chain(
    "SPY",
    params={
        "strike_price.lte": 673,
        "expiration_date": "2025-10-10",
        "contract_type": "put",
        "order": "desc",
        "limit": 10,
        "sort": "strike_price",
    },
):
    options_chain.append(o)

print(options_chain)
"

Here is the example Polygon Endpoint Call full response that is UNFORMATTED.  So AI Agent will need to re-format and ONLY respond with the requested output formatting previously specified.  The full options chain is very verbose with alot of not needed details, so the formated response strips out and only shows the essential info.

"
{
  "results": [
    {
      "day": {
        "change": -2.82,
        "change_percent": -62.7,
        "close": 1.68,
        "high": 4.34,
        "last_updated": 1759896000000000000,
        "low": 1.68,
        "open": 3.77,
        "previous_close": 4.5,
        "volume": 22280,
        "vwap": 2.0937
      },
      "details": {
        "contract_type": "put",
        "exercise_style": "american",
        "expiration_date": "2025-10-10",
        "shares_per_contract": 100,
        "strike_price": 673,
        "ticker": "O:SPY251010P00673000"
      },
      "greeks": {
        "delta": -0.4825557268049289,
        "gamma": 0.09196020791368768,
        "theta": -0.4722749362227307,
        "vega": 0.18863870943786484
      },
      "implied_volatility": 0.09336299064337816,
      "open_interest": 3139,
      "underlying_asset": {
        "ticker": "SPY"
      }
    },
    {
      "day": {
        "change": -2.57,
        "change_percent": -65.2,
        "close": 1.37,
        "high": 3.76,
        "last_updated": 1759896000000000000,
        "low": 1.36,
        "open": 3.28,
        "previous_close": 3.94,
        "volume": 42831,
        "vwap": 1.7976
      },
      "details": {
        "contract_type": "put",
        "exercise_style": "american",
        "expiration_date": "2025-10-10",
        "shares_per_contract": 100,
        "strike_price": 672,
        "ticker": "O:SPY251010P00672000"
      },
      "greeks": {
        "delta": -0.39979906781434793,
        "gamma": 0.08257718531492517,
        "theta": -0.484633849698867,
        "vega": 0.18775071527566894
      },
      "implied_volatility": 0.09931649848437918,
      "open_interest": 6509,
      "underlying_asset": {
        "ticker": "SPY"
      }
    },
    {
      "day": {
        "change": -2.27,
        "change_percent": -66.8,
        "close": 1.13,
        "high": 3.25,
        "last_updated": 1759896000000000000,
        "low": 1.12,
        "open": 2.82,
        "previous_close": 3.4,
        "volume": 21707,
        "vwap": 1.7976
      },
      "details": {
        "contract_type": "put",
        "exercise_style": "american",
        "expiration_date": "2025-10-10",
        "shares_per_contract": 100,
        "strike_price": 671,
        "ticker": "O:SPY251010P00671000"
      },
      "greeks": {
        "delta": -0.33166632563716564,
        "gamma": 0.0725094592342699,
        "theta": -0.498455460257641,
        "vega": 0.1638105346753274
      },
      "implied_volatility": 0.10705730707245131,
      "open_interest": 10084,
      "underlying_asset": {
        "ticker": "SPY"
      }
    },
    {
      "day": {
        "change": -2.02,
        "change_percent": -68.2,
        "close": 0.94,
        "high": 2.81,
        "last_updated": 1759896000000000000,
        "low": 0.94,
        "open": 2.39,
        "previous_close": 2.96,
        "volume": 41728,
        "vwap": 1.4997
      },
      "details": {
        "contract_type": "put",
        "exercise_style": "american",
        "expiration_date": "2025-10-10",
        "shares_per_contract": 100,
        "strike_price": 670,
        "ticker": "O:SPY251010P00670000"
      },
      "greeks": {
        "delta": -0.2772046848683708,
        "gamma": 0.062178885848669777,
        "theta": -0.48663851031398286,
        "vega": 0.16318657164604886
      },
      "implied_volatility": 0.11395401502078724,
      "open_interest": 11767,
      "underlying_asset": {
        "ticker": "SPY"
      }
    },
    {
      "day": {
        "change": -1.79,
        "change_percent": -69.4,
        "close": 0.79,
        "high": 2.39,
        "last_updated": 1759896000000000000,
        "low": 0.79,
        "open": 2.06,
        "previous_close": 2.58,
        "volume": 12346,
        "vwap": 1.2711
      },
      "details": {
        "contract_type": "put",
        "exercise_style": "american",
        "expiration_date": "2025-10-10",
        "shares_per_contract": 100,
        "strike_price": 669,
        "ticker": "O:SPY251010P00669000"
      },
      "greeks": {
        "delta": -0.23152045294425277,
        "gamma": 0.05340494764729266,
        "theta": -0.4821399561094331,
        "vega": 0.162805063413914
      },
      "implied_volatility": 0.12211118120644916,
      "open_interest": 5397,
      "underlying_asset": {
        "ticker": "SPY"
      }
    },
    {
      "day": {
        "change": -1.58,
        "change_percent": -69.9,
        "close": 0.68,
        "high": 2.06,
        "last_updated": 1759896000000000000,
        "low": 0.67,
        "open": 1.75,
        "previous_close": 2.26,
        "volume": 21602,
        "vwap": 1.2248
      },
      "details": {
        "contract_type": "put",
        "exercise_style": "american",
        "expiration_date": "2025-10-10",
        "shares_per_contract": 100,
        "strike_price": 668,
        "ticker": "O:SPY251010P00668000"
      },
      "greeks": {
        "delta": -0.19652209027630926,
        "gamma": 0.04560201399915712,
        "theta": -0.4594949520582037,
        "vega": 0.12426779766020168
      },
      "implied_volatility": 0.1288327233420103,
      "open_interest": 8411,
      "underlying_asset": {
        "ticker": "SPY"
      }
    },
    {
      "day": {
        "change": -1.39,
        "change_percent": -70.2,
        "close": 0.59,
        "high": 1.76,
        "last_updated": 1759896000000000000,
        "low": 0.58,
        "open": 1.49,
        "previous_close": 1.98,
        "volume": 9448,
        "vwap": 0.995
      },
      "details": {
        "contract_type": "put",
        "exercise_style": "american",
        "expiration_date": "2025-10-10",
        "shares_per_contract": 100,
        "strike_price": 667,
        "ticker": "O:SPY251010P00667000"
      },
      "greeks": {
        "delta": -0.16753784432123148,
        "gamma": 0.03890622718133649,
        "theta": -0.4373917225825099,
        "vega": 0.12402997297108903
      },
      "implied_volatility": 0.13592757875452868,
      "open_interest": 7213,
      "underlying_asset": {
        "ticker": "SPY"
      }
    },
    {
      "day": {
        "change": -1.21,
        "change_percent": -69.5,
        "close": 0.53,
        "high": 1.5,
        "last_updated": 1759896000000000000,
        "low": 0.5,
        "open": 1.3,
        "previous_close": 1.74,
        "volume": 10815,
        "vwap": 0.8302
      },
      "details": {
        "contract_type": "put",
        "exercise_style": "american",
        "expiration_date": "2025-10-10",
        "shares_per_contract": 100,
        "strike_price": 666,
        "ticker": "O:SPY251010P00666000"
      },
      "greeks": {
        "delta": -0.1452436735092106,
        "gamma": 0.03334894768675657,
        "theta": -0.4280105029514677,
        "vega": 0.1238923214438963
      },
      "implied_volatility": 0.1450713728428117,
      "open_interest": 6189,
      "underlying_asset": {
        "ticker": "SPY"
      }
    },
    {
      "day": {
        "change": -1.08,
        "change_percent": -70.1,
        "close": 0.46,
        "high": 1.29,
        "last_updated": 1759896000000000000,
        "low": 0.42,
        "open": 1.13,
        "previous_close": 1.54,
        "volume": 16843,
        "vwap": 0.6491
      },
      "details": {
        "contract_type": "put",
        "exercise_style": "american",
        "expiration_date": "2025-10-10",
        "shares_per_contract": 100,
        "strike_price": 665,
        "ticker": "O:SPY251010P00665000"
      },
      "greeks": {
        "delta": -0.12630295469727104,
        "gamma": 0.028799978481793824,
        "theta": -0.4174313165861396,
        "vega": 0.08276238782548204
      },
      "implied_volatility": 0.15402160094478062,
      "open_interest": 14874,
      "underlying_asset": {
        "ticker": "SPY"
      }
    },
    {
      "day": {
        "change": -0.95,
        "change_percent": -69.3,
        "close": 0.42,
        "high": 1.11,
        "last_updated": 1759896000000000000,
        "low": 0.39,
        "open": 0.96,
        "previous_close": 1.37,
        "volume": 6471,
        "vwap": 0.6506
      },
      "details": {
        "contract_type": "put",
        "exercise_style": "american",
        "expiration_date": "2025-10-10",
        "shares_per_contract": 100,
        "strike_price": 664,
        "ticker": "O:SPY251010P00664000"
      },
      "greeks": {
        "delta": -0.11211324881741162,
        "gamma": 0.02504232443730556,
        "theta": -0.3979322047644065,
        "vega": 0.08243997192206928
      },
      "implied_volatility": 0.1611832878652526,
      "open_interest": 5064,
      "underlying_asset": {
        "ticker": "SPY"
      }
    }
  ],
  "status": "OK",
  "request_id": "21c86c2a5ea0225351d02447600852bc",
  "next_url": "https://api.polygon.io/v3/snapshot/options/SPY?cursor=YXA9TyUzQVNQWTI1MTAxMFAwMDY2NDAwMCZhcz0mY29udHJhY3RfdHlwZT1wdXQmZXhwaXJhdGlvbl9kYXRlPTIwMjUtMTAtMTAmbGltaXQ9MTAmb3JkZXI9ZGVzYyZzb3J0PXN0cmlrZV9wcmljZSZzdHJpa2VfcHJpY2UubHRlPTY2NC4wMDAwMDA"
}
"

3. Add new test cases in 'test_cli_regression.sh' as follows:
 Add 2x test cases after SPY Test Sequence Technical Analysis test case:
- "Get the SPY Call Options Chain Expiring this Friday"
- "Get the SPY Put Options Chain Expiring this Friday"

Add 2x test cases after NVDA Test Sequence Technical Analysis test case:
- "Get the NVDA Call Options Chain Expiring this Friday"
- "Get the NVDA Put Options Chain Expiring this Friday"

4. Validate by running 1x loop of 'test_cli_regression.sh' AND ACTUALLY VIEW THE RESPONSES AND DO NOT BLINDLY JUST SEE TEST PASSED WITHOUT SEEING THE ACTUAL CONTENT.  Fix any issues in code and\or script if needed After validating notify user to review results first, so do NOT proceed with serenea updates or commits yet until user reviews the latest test results of your fixes to confirm the issues are trul fixed or not.

---

<Planning Phase> 🔴 CRITICAL: DO NOT START ANY IMPLEMENTATION DURING THIS PHASE 🔴

Based on the Research, Analysis & Scoping from previous task(s), delete the current file 'TODO_task_plan.md' and then create a brand new granular detailed Implementation Plan TODO Task Checklist file 'TODO_task_plan.md' for you to systemtically use your Mandatory Tools Toolkit for Sequential-Thinking & Serena tools to Implement the requested task(s) with Comprehensive Documentation Updates to reflect the latest updates to remove outdated info, and You MUST create a CLI Testing Phase as part of the Plan to run testing to validate any code changes.  The plan MUST enforce that YOU MUST Systemtically use your Mandatory Tools Toolkit Sequential-Thinking & Serena tools to enhance your workflow to perform all task(s)

---

<Implementation Phase>

You MUST Systemtically use your Mandatory Tools Toolkit Sequential-Thinking & Serena tools to Implement all code changes, test suite updates, and agent instruction modifications according to the TODO_task_plan.md

---

<CLI Testing Phase> 🔴 MANDATORY CHECKPOINT - DO NOT SKIP 🔴

⚠️ **CRITICAL: You MUST run tests BEFORE claiming completion** ⚠️
⚠️ **CRITICAL: Task is INCOMPLETE without test execution and results** ⚠️

**REQUIRED ACTIONS:**

1. ✅ **Execute the test suite:**

   ```bash
   ./test_cli_regression.sh
   ```

2. ✅ **Verify test results:**
   - All tests PASS (must show 100% success rate)
   - Test report generated in test-reports/
   - No errors or failures in output
   - Session persistence verified

3. ✅ **Show evidence to user:**
   - Display test summary output
   - Show pass/fail counts (must be X/X PASS)
   - Provide test report file path
   - Show performance metrics (response times)

**❌ ENFORCEMENT RULES:**

- Code without test execution = Code NOT implemented
- No test results = Task INCOMPLETE
- Must run tests BEFORE Serena memory update phase
- Cannot claim "done" without showing test evidence
- Test failures must be fixed and re-tested

**✅ ONLY PROCEED to next phase after:**

- Test suite executed successfully
- 100% pass rate achieved
- Test results displayed to user
- Test report path provided

🔴 **IF YOU SKIP THIS PHASE, THE ENTIRE TASK IS INVALID** 🔴

---

<Serena Update Memories Phase>

Update Serena memory files with new tool information, architecture changes, and test results (ONLY after tests pass)

---

<Final Git Commit Phase> 🔴 CRITICAL: PROPER ATOMIC COMMIT WORKFLOW 🔴

**MANDATORY: Stage ONLY Immediately Before Commit**

**CORRECT Workflow (follow EXACTLY):**

1. **DO ALL WORK FIRST** (DO NOT stage anything yet):
   - ✅ Complete ALL code changes
   - ✅ Run ALL tests and generate test reports
   - ✅ Update ALL documentation (CLAUDE.md, tech_stack.md, etc.)
   - ✅ Update ALL config files (.claude/settings.local.json, etc.)
   - ✅ Update ALL Serena memories
   - ✅ Update ALL task plans
   - ⚠️ **DO NOT RUN `git add` YET**

2. **VERIFY EVERYTHING IS COMPLETE**:

   ```bash
   git status  # Review ALL changed/new files
   git diff    # Review ALL changes
   ```

   - Ensure ALL work is done
   - Ensure ALL files are present

3. **STAGE EVERYTHING AT ONCE**:

   ```bash
   git add -A  # Stage ALL files in ONE command
   ```

   - ⚠️ This is the FIRST time you run `git add`
   - ⚠️ Stage ALL related files together

4. **VERIFY STAGING IMMEDIATELY**:

   ```bash
   git status  # Verify ALL files staged, NOTHING unstaged
   ```

   - If anything is missing: `git add [missing-file]`

5. **COMMIT IMMEDIATELY** (within 60 seconds of staging):

   ```bash
   git commit -m "$(cat <<'EOF'
   [TAG] Descriptive commit message

   - Change 1
   - Change 2

   🤖 Generated with [Claude Code](https://claude.com/claude-code)

   Co-Authored-By: Claude <noreply@anthropic.com>
   EOF
   )"
   ```

6. **PUSH IMMEDIATELY**:

   ```bash
   git push
   ```

**WHAT BELONGS IN ATOMIC COMMIT:**

- ✅ Code changes (backend + frontend)
- ✅ Test reports (evidence of passing tests)
- ✅ Documentation updates (CLAUDE.md, README.md, etc.)
- ✅ Memory updates (.serena/memories/)
- ✅ Config changes (.claude/settings.local.json, etc.)
- ✅ Task plan updates (TODO_task_plan.md, etc.)

**❌ NEVER DO THIS:**

- ❌ Stage files early during development
- ❌ Stage files "as you go"
- ❌ Run `git add` before ALL work is complete
- ❌ Delay between `git add` and `git commit`
- ❌ Commit without test reports
- ❌ Commit without documentation updates

**Reference:** See `.serena/memories/git_commit_workflow.md` for complete details

---
