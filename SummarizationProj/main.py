from fastapi import FastAPI
import uvicorn
from starlette.middleware.cors import CORSMiddleware
from model import Input
from utils.youtube import getVidInfos
from transformers.models.bart import BartForConditionalGeneration
from transformers import PreTrainedTokenizerFast
import torch

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_credentials=True, allow_methods=['*'], allow_headers=["*"])
def load_model():
    model = BartForConditionalGeneration.from_pretrained('C:/Users/Main/학회/플젝/SummarizationProj/KoBART-summarization/transformer_model')
    # tokenizer = get_kobart_tokenizer()
    return model
model = load_model()
tokenizer = PreTrainedTokenizerFast.from_pretrained('gogamza/kobart-base-v1')
def infer(text: str):
    input_ids = tokenizer.encode(text)
    input_ids = torch.tensor(input_ids)
    input_ids = input_ids.unsqueeze(0)
    output = model.generate(input_ids, eos_token_id=1, max_length=512, num_beams=5)
    output = tokenizer.decode(output[0], skip_special_tokens=True)
    return output
def returnResult(text):
    txtLength = len(text)
    txtLen = txtLength // 1000 + 1
    txtArray = list()
    for i in range(txtLen):
        if i == txtLen-1:
            txtArray.append(text[1000*i:])
        else:
            txtArray.append(text[1000*i:1000*(i+1)])
    outputArray = list()
    for txt in txtArray:
        output = infer(txt)
        outputArray.append(output)
    return outputArray





@app.post("/getVidInfo")
def vidInfo(input : Input):
    url = input.url
    title, thumbnail, channel, description, caption_text = getVidInfos(url)
    return {
        "title" : title,
        "thumbnail" : thumbnail,
        "channel" : channel,
        "description" : description,
        "caption_text" : caption_text
    }
@app.post("/getSummarization")
def returnSummarization(input : Input):
    text = input.text
    result = returnResult(text)
    return {
        "result" : result
    }

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)