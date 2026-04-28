from typing import TypedDict, Optional
from pydantic import BaseModel, Field


class State(TypedDict):
    message:          str
    message_category: Optional[str]
    answer:           Optional[str]


class MessageClassifier(BaseModel):
    category: str = Field(
        description="""
        Classify the customer message into exactly one of these categories:

        - PRODUCT_INQUIRY: customer asks about a product.
          Examples: 'Is the blue jacket available in XL?',
                    'What is the price of white sneakers?',
                    'Do you have this in size M?'

        - ORDER_REQUEST: customer wants to place an order.
          Examples: 'I want to order a black hoodie size L',
                    'I would like to buy 2 pieces of the red jacket'

        - NEED_HUMAN: customer has a complaint or sensitive request.
          Examples: 'I received the wrong item',
                    'I want a refund',
                    'My order never arrived'

        - IRRELEVANT: message is not related to the store.
          Examples: 'How are you?', 'What time is it?', 'Tell me a joke'

        Reply with only one word: PRODUCT_INQUIRY, ORDER_REQUEST, NEED_HUMAN, or IRRELEVANT.
        """
    )


class OrderDetails(BaseModel):
    product_name:  str = Field(description="Name of the product to order e.g. 'Black Hoodie'")
    size:          str = Field(description="Size of the product e.g. 'S', 'M', 'L', 'XL', '42'")
    color:         str = Field(description="Color of the product e.g. 'Blue', 'Black', 'Red'")
    quantity:      int = Field(description="Number of pieces the customer wants to order e.g. 1, 2, 3")
    customer_name: str = Field(description="Full name of the customer e.g. 'Ahmed Zerroug'")