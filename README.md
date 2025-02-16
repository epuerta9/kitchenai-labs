# 🚀 KitchenAI Bento Demo


> **⚠️ IMPORTANT NOTE:** When making changes to your Bento within a Jupyter notebook, you must interrupt and restart the kernel to prevent duplicate connections. This requirement only applies when using Jupyter notebooks and not when using the whisk CLI. For the purposes of this demo, we'll be using Jupyter notebooks.


Welcome to the **KitchenAI Bento Box Demo!** 🍱  
This notebook will walk you through the process of setting up, connecting, and interacting with a **KitchenAI Bento Box**—your modular AI powerhouse.  

By the end of this guide, you'll have:  
✅ A working **KitchenAI control plane**  
✅ Your first **Bento Box** connected  
✅ A hands-on experience with querying and managing AI models in **KitchenAI**

---

## 🛠️ Prerequisites

Before we dive in, make sure you've set up your environment:

### 1️⃣ Create a Virtual Environment  

Run the following command in your terminal:

```bash
python -m venv venv
```

Then activate it:  
- **Mac/Linux**: `source venv/bin/activate`  
- **Windows**: `venv\Scripts\activate`

### 2️⃣ Start the KitchenAI Control Plane  

You'll need to spin up the KitchenAI control plane. Follow the instructions in the  [KitchenAI self hosting control plane section](https://github.com/epuerta9/kitchenai?tab=readme-ov-file#self-hosting-the-control-plane) to get it running. Once done, your local control plane should be available at:

🔗 **Dashboard:** [http://localhost:8001](http://localhost:8001)

---

## 🏗️ Step 1: Connecting Your First Bento Box  

Now, let's bring our **first Bento Box** to life! 

1️⃣ Open `bento.ipynb` in Jupyter Notebook.  
2️⃣ Select the **virtual environment (venv)** you created as the kernel.  
3️⃣ Run all the cells.  

If everything works correctly, your **Bento Box should now be connected** 🎉. You can verify this by checking the **KitchenAI Dashboard** at [http://localhost:8001](http://localhost:8001).  

At this stage, your Bento Box is active, but **no files have been uploaded yet**. Let's change that!

> NOTE: keep your notebook cell running, its a blocking process because the bento box has to establish a constant connection to the control plane

---

## 📡 Step 2: Interacting with Bento Boxes via the Client Notebook  

The **client_playground.ipynb** notebook is where the magic happens. It allows you to **interact with your Bento Boxes** through the KitchenAI control plane.  

**Why is it so easy to use?**  
It follows the familiar structure of the **OpenAI Python SDK**, making it intuitive for AI developers!  

### 🔥 Example: Running a Query  

```python
chat_extra_body = ChatExtraBody(
    namespace="my-remote-client",
    version="1.0.0",
)   

print(chat_extra_body.model_dump())

response = client.chat.completions.create(
    model="@<clientid>/query-no-rag", # Replace <clientid> with your actual client ID
    messages=[{"role": "user", "content": "What's the most important part of the README?"}],
    metadata={"user_id": "123"},
    extra_body=chat_extra_body.model_dump()
)

print(response)
```

---

## 📌 Step 3: Uploading & Querying Files  

Now that our Bento Box is running, let’s interact with it!

✅ **Upload a file** using the `@<clientid>/<label>` convention.  
✅ **Verify the file exists** using the **files API**.  
✅ **Run a chat completion query** using a **non-RAG Bento label**.  
✅ **Run a chat completion query** using a **RAG-enabled Bento label**.  
✅ **Delete the file** from the object store.  

By following these steps, you'll be able to **upload, process, and query your own data** inside KitchenAI—empowering you to build AI-powered applications faster than ever.  

---

## 🎯 Ready to Build?  

You’re now equipped to **deploy and interact with your own KitchenAI Bento Boxes!** 🚀  

💡 **Next Steps:**  
- Experiment with **different Bento labels** and configurations.  
- Explore **RAG (Retrieval-Augmented Generation) workflows**.  
- Try **integrating KitchenAI with your existing AI projects**.  

For further details, check out the [KitchenAI repository](https://github.com/epuerta9/kitchenai) or join our community to share your Bento Box creations! 🚀🔥  



