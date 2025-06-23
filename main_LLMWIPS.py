import json
import os
import random
import accelerate
# Load model directly
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
random.seed(42)

#quantization_config = BitsAndBytesConfig(load_in_4bit=True)
tokenizer = AutoTokenizer.from_pretrained("deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B") #change this to your model path
model = AutoModelForCausalLM.from_pretrained("deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B") #change this to your model path

real_path = "./distribution/part_"

def walk_directory(directory):
    l = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".json"):
                l.append(os.path.join(root, file))
    return l

def get_topic(path):
    topic =''
    with open(path, "r") as f:
        data = json.load(f)
        topic = data["topic"]
    return topic

def choose_random_article():
    real_path = "./distribution/"
    all_files = walk_directory(real_path)
    random_file = random.choice(all_files)
    return random_file

#select a random article and extract its topic. Based on the topic, select a list of 10 random tokens from the common tokens that are related to the topic
def select_random_tokens_for_topic(topic, common_tokens, num_tokens=10):
    related_tokens = [token for token, data in common_tokens.items() if topic in data["topic"]]
    if len(related_tokens) < num_tokens:
        print(f"Not enough related tokens for topic '{topic}'. Found: {len(related_tokens)}")
        return related_tokens
    return random.sample(related_tokens, num_tokens)

def main():
    random_article = choose_random_article()
    topic = get_topic(random_article)
    print(f"Selected article path: {random_article}")
    print(f"Randomly selected article topic: {topic}")
    
    common_tokens_file = "./json_files/new_tokenizer_tests/common_tokens.json"
    with open(common_tokens_file, "r") as f:
        common_tokens = json.load(f)
    selected_tokens = select_random_tokens_for_topic(topic, common_tokens)
    print(f"Selected tokens related to topic '{topic}': {selected_tokens}")
    #save the key facts and the additional facts from the article in two varibles
    with open(random_article, "r") as f:
        article_data = json.load(f)
        key_facts = article_data.get("key_facts", [])
        other_facts = article_data.get("other_facts", [])
        #choose 5 random other facts
        if len(other_facts) > 5:
            other_facts = random.sample(other_facts, 5)
        else:
            print(f"Not enough other facts. Found: {len(other_facts)}")
    print(f"Key facts: {key_facts}")
    print(f"Other facts: {other_facts}")

    kf_prompt = ", ".join(key_facts)
    of_prompt = ", ".join(other_facts)
    st_prompt = ", ".join(selected_tokens)

    prompt = f"""You are an AI assistant tasked with generating an article based on the following key facts (included in <keyfacts></keyfacts> tags) and additional facts (included in <additionalfacts></additionalfacts> tags). Use the provided tokens (included in <tokens></tokens> tags) as much as you can to enhance the article's content and ensure it is relevant to the topic '{topic}'.
Key Facts: <keyfacts>{kf_prompt}</keyfacts>
Additional Facts: <additionalfacts>{of_prompt}</additionalfacts>
Tokens to use: <tokens>{st_prompt}</tokens>
Please generate a coherent and informative article that incorporates these elements."""
    return prompt

if __name__ == "__main__":
    for i in range(100):
        prompt = main()
        print(f"Step_{i} --- \nGenerated Prompt:")
        print(f'{prompt}\n')
        with open('./json_files/new_tokenizer_tests/prompts/generated_prompt_'+f'{i}'+'.txt', "w") as f:
            f.write(prompt)

        # Here you call the model to generate the article based on the prompt.
        model_inputs = tokenizer([prompt], return_tensors="pt").to("auto")
        generated_ids = model.generate(**model_inputs)
        tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
        generated_text = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]

        with open('./json_files/new_tokenizer_tests/prompts/generated_article_'+f'{i}'+'.txt', "w") as f:
            f.write(generated_text)
        print("\n")