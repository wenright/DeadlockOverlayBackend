Repo for training an image classifier on Deadlock item icons.

## Running
requires python 3.8

`pip install -r requirements.txt`

`python src/train.py`


## Pulling more icon data
`python src/item_puller.py`

Fetches item screenshots from the stream defined there, then pull up a window with a guess as to what the item is. Just hit enter if it looks right, or type the name if it's wrong. Data will be written to `data/training_data/[item_name]`

You may notice that `output/full.png` is not the right stream, but a Twtich preroll instead. The only way I've found to bypass this is by signing up for twitch turbo, then adding your auth token to `src/.env` in the format `TWITCH_AUTH=[your_auth]`. Find out how to get your auth token [here](https://streamlink.github.io/cli/plugins/twitch.html).

## Sweeps
[Most recent sweep](https://api.wandb.ai/links/wenright0-self/8h0pe1bz)

`wandb agent [agent_id]` 

Runs a Weights & Biases sweep over some hyper parameters defined in sweep.yaml, which can help find optimal values. You'll need to sign in to wandb first with `wandb login`, then set up a sweep in your account on the site, and copy/paste the contents of sweep.yaml into the sweep configuration on creation.


