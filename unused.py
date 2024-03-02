import tiktoken

def num_tokens_from_messages(messages, model="gpt-3.5-turbo-0613"):
    """Return the number of tokens used by a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        print("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")
    if model in {
        "gpt-3.5-turbo-0613",
        "gpt-3.5-turbo-16k-0613",
        "gpt-4-0314",
        "gpt-4-32k-0314",
        "gpt-4-0613",
        "gpt-4-32k-0613",
        }:
        tokens_per_message = 3
        tokens_per_name = 1
    elif model == "gpt-3.5-turbo-0301":
        tokens_per_message = 4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
        tokens_per_name = -1  # if there's a name, the role is omitted
    elif "gpt-3.5-turbo" in model:
        print("Warning: gpt-3.5-turbo may update over time. Returning num tokens assuming gpt-3.5-turbo-0613.")
        return num_tokens_from_messages(messages, model="gpt-3.5-turbo-0613")
    elif "gpt-4" in model:
        print("Warning: gpt-4 may update over time. Returning num tokens assuming gpt-4-0613.")
        return num_tokens_from_messages(messages, model="gpt-4-0613")
    else:
        raise NotImplementedError(
            f"""num_tokens_from_messages() is not implemented for model {model}. See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens."""
        )
    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
    return num_tokens

# ["MB:Rent Feb 2023 " ,"23500.0"],["UPI/MYGATE/403239015739/Dues settle" ,"3909.0"],["UPI/SHARATH KUMAR S/403446621899/Pay to BharatPe " ,"210.0"],["UPI/SUN TV NETWORK /440090056305/SUNTVNETWORKLIM " ,"799.0"],["UPI/mohankumaarrr@o/440295538741/UPI " ,"1500.0"],["UPI/SWIGGY/440340324838/Debit Money Usi" ,"149.0"],["PCD/4171/DINDIGUL THALAPPAKATTI/VILLUP080224/16:21 " ,"1502.0"],["UPI/aanurag.singh19/404093737214/UPI " ,"50000.0"],["UPI/aanurag.singh19/404038435072/UPI " ,"50000.0"],["MB:transfer to PNB " ,"10000.0"],["MB:i dont want ur money" ,"200000.0"],["UPI/mohanraajjj@oka/404229089396/UPI " ,"5000.0"],["UPI/mohanraajjj@oka/440874584250/UPI " ,"10000.0"],["UPI/CHANNAHALLI RAJ/440873522917/DD" ,"810.0"],["UPI/WATTAPP TECHNOL/404489972222/Paymentforcharg " ,"500.0"],["UPI/CHANNAHALLI RAJ/404413312877/DD" ,"2410.0"],["UPI/Zerodha Broking/404586451269/784914363646222 " ,"40000.0"],["UPI/mohankumaarrr@o/441155796013/UPI " ,"1500.0"],["UPI/JEEVARATHINAM/441163035336/Transfer to Mom " ,"10000.0"],["UPI/Blinkit/441407122608/OidZTBLINUPIC24 " ,"366.0"],["UPI/CHANNAHALLI RAJ/404846087470/DD" ,"2900.0"],["MB:Ramya transfer" ,"100000.0"],["UPI/Amazon India/405121071639/You are paying " ,"1577.0"],["UPI/NIROOP PUKALE/405156620804/UPI " ,"50000.0"],["UPI/NIROOP PUKALE/405150619741/UPI " ,"50000.0"]