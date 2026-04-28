from tools import *
from state import *
from prompt import *
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.graph import START , END , StateGraph

load_dotenv()
llm = ChatGroq(model="llama-3.3-70b-versatile")


def classify_node(State: dict)->dict:
    question = State["message"]
    response = llm.with_structured_output(MessageClassifier).invoke([
        {"role":"system" , "content":classifier_prompt()},
        {"role":"user" , "content": question},
    ])
    return {"message_category": response.category}


def product_inquiry_node(State: dict)->dict:
    question = State["message"]
    product_data = get_all_products()
    response = llm.invoke([
        {"role": "system", "content": product_inquiry_prompt(product_data)},
        {"role": "user", "content": question},
    ])
    return {"answer": response.content}



def order_node(state: dict) -> dict:
    message = state["message"]

    # extract order details from customer message
    order = llm.with_structured_output(OrderDetails).invoke([
        {"role": "system", "content": order_prompt()},
        {"role": "user",   "content": message}
    ])

    # place order in database
    result = place_order(
        customer_name=order.customer_name,
        customer_email="",
        product_name=order.product_name,
        size=order.size,
        color=order.color,
        quantity=order.quantity,
        price=0
    )

    return {"answer": result}



def need_human_node(State: dict)->dict:
    message = State["message"]
    notify_manager(message,"")
    answer = llm.invoke([
        {"role":"system" , "content":need_human_prompt()},
        {"role": "user", "content": message},
    ])
    return {"answer": answer.content}


graph = StateGraph(State)

def router(state: dict) -> dict:
    category = state["message_category"]
    return category



graph.add_node("classifier",classify_node)
graph.add_node("product",product_inquiry_node)
graph.add_node("order",order_node)
graph.add_node("customer",need_human_node)

graph.add_edge(START,"classifier")
graph.add_conditional_edges(
    "classifier",
    router ,
    {
    "PRODUCT_INQUIRY":"product",
    "ORDER_REQUEST":"order",
    "NEED_HUMAN":"customer",
    "IRRELEVANT": END
    }
)

graph.add_edge("product", END)
graph.add_edge("order", END)
graph.add_edge("customer", END)

chatbot = graph.compile()

def ask(message: str) -> str:
    result = chatbot.invoke({
        "message":          message,
        "message_category": None,
        "answer":           None
    })
    return result["answer"]


# ── Test locally ──────────────────────────────────────────────
if __name__ == "__main__":
    print(ask("Do you have a black hoodie in size L?"))
    print(ask("I want to order 2 blue t-shirts size M"))
    print(ask("I received the wrong item"))
    print(ask("What is the weather today?"))
