# How to use
1. Generate your unique client id and Oauth token via Twitch Developers.
2. Replace it with `---client-id---` and `---oauth-token---` in `main.py`.
3. Replace `---required-video-length---` with the desired length in minutes in `main.py`.
4. In `get_clips()` function , replace ` game = ---here--- ` in `get_top()` method to required game, if you specify <br>
`channel = ---here--- ` parameter, it will override the game parameter.

You are good to go.
