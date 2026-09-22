# Jev Demo — Typed Decisions via Vercel AI Gateway

A tiny Python example that calls **Jev** (TypeSafe AI's decision model) through
the **Vercel AI Gateway**. Instead of chatting, Jev evaluates some `state`
against typed `questions` and returns a structured answer with confidence.

This demo asks: **What is a fruit? — `apple` or `truck`**

```
Question : what is a fruit?  1: apple   2: truck
Jev says : apple is the fruit.   (confidence 1.0)
```

## Get an API key

1. Go to the Jev model page: <https://vercel.com/ai-gateway/models/jev>
2. Click **Get API key**, create one for your team, and copy the `vck_...` value.
3. Jev is **free**, but Vercel needs a payment method on your team to unlock the
   free credits before it serves requests (this demo costs a fraction of a cent).

## Run

```bash
pip install requests
export AI_GATEWAY_API_KEY="vck_your_key_here"   # or put it in ai-gateway.txt
python jev_demo.py
```

> Never commit your key — keep `ai-gateway.txt` in `.gitignore`.

## How it works

One HTTP POST to `https://ai-gateway.vercel.sh/typesafe/v1/systemone` with model
`typesafe-ai/jev`, a `state` string, and typed `questions`. Question types:
`choice` (pick one option), `noul` (yes/no probability), `score` (a number).
Edit `state` and `questions` in `jev_demo.py` to ask your own.

## Reference

<https://vercel.com/ai-gateway/models/jev>
