# Multi-Party Dialogue Dataset (MPDD)
MPDD dataset contains 4,142 dialogues and 25,548 utterances. Each utterance was annotated with the emotion label, the list of the listeners and the relation between the speaker and listener.

## Create dataset
```
pip3 install -r requirements.txt
python3 build_MPDD.py --data_dir ./data/ --output_dir ./
```
