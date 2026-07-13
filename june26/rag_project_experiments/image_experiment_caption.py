"""This module will containe the code for image captioning
"""
from langchain_core.messages import HumanMessage, SystemMessage
from utils import get_model_from_gcp, image_to_base64
from langchain_core.prompts import ChatPromptTemplate

llm = get_model_from_gcp()

# To add image to the prompt we need to send the base64 encoded version of bytes

image = image_to_base64("./images/page_1_1.jpeg")



prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an expert in captioning images extracted from NCERT textbooks.
Use the page content to understand the context of the image.
Generate educational captions suitable for the student's grade level.
"""
        ),
        (
            "human",
            [
                {
                    "type": "text",
                    "text": """
Subject: {subject}

Standard: {standard}

Page Content:
{content}

Generate a caption for the attached image.
"""
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "data:image/png;base64,{image}"
                    }
                }
            ]
        )
    ]
)


chain = prompt | llm

result = chain.invoke({
    "image": image,
    "subject": "mathematics",
    "standard": "7",
    "content": """1.1 A Lakh Varieties!
Eshwarappa is a farmer in Chintamani, 
a town in Karnataka. He visits the 
market regularly to buy seeds for his 
rice field. During one such visit he 
overheard a conversation between 
Ramanna and Lakshmamma. Ramanna 
said, “Earlier our country had about a 
lakh varieties of rice. Farmers used to 
preserve different varieties of seeds 
and use them to grow rice. Now, we 
only have a handful of varieties. Also, 
farmers have to come to the market to buy seeds”.
Lakshmamma said, “There is a seed bank near my house. So far, they 
have collected about a hundred indigenous varieties of rice seeds from 
different places. You can also buy seeds from there.”
You may have heard the word ‘lakh’ 
before. Do you know how big one lakh is? Let 
us find out.
Eshwarappa shared this incident with his 
daughter Roxie and son Estu .
Estu was surprised to know that there 
were about one lakh varieties of rice in this 
country. He wondered “One lakh! So far I 
have only tasted 3 varieties. If we tried a new 
variety each day, would we even come close 
to tasting all the varieties in a lifetime of 100 
years?”
What do you think? Guess.
LARGE NUMBERS 
AROUND US
1
Reprint 2026-27

"""
})
print(result.content)
