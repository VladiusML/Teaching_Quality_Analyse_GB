# Оценка качества преподавания
Мы представляем наше решение кейса "Оценка качества преподавания"

## Структура проекта

## Гайд по запуску
>[!IMPORTANT]
>Мы подготовили 2 версии процессинга текста сообщений: через `langchain🦜` и `🤗 Transformers`. Суть орбаботки через `langchain` состоит в локальной загрузке `llmки` из `🤗 Hub`([saiga](https://huggingface.co/IlyaGusev/saiga_llama3_8b)/[vikhr](https://huggingface.co/Vikhrmodels/Vikhr-7b-0.1)/[mistral](https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.2))
>и дальнейшего её промптинга для анализа текста на соответсвие конкретной теме. Но для таких тяжёлых моделей у нас не хватило вычислительных мощностей - одно текстовое сообщение могло обрабтываться несколько минут(запускали на CPU). Поэтому мы перешли
>на второй вариант - zero-shot-classification с помощью [mDeBERTa](https://huggingface.co/MoritzLaurer/mDeBERTa-v3-base-mnli-xnli)

 1. Установите зависимости
```
pip install -r requirements.txt
```
