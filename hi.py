from transformers import MBartForConditionalGeneration, MBart50TokenizerFast

model_name = "facebook/mbart-mini-50"
tokenizer = MBart50TokenizerFast.from_pretrained(model_name)
model = MBartForConditionalGeneration.from_pretrained(model_name)

tokenizer.save_pretrained("models/mbart-mini-50")
model.save_pretrained("models/mbart-mini-50")