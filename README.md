# pealbot
Pealbot is a simple IRC bot framework written in python. It uses plugins for every function and is thus easy to advance.
The main configuration including server, channel, username and so on can be found in the launcher (pealbot.py).

At the moment it supports:
- switching channels
- add strings to queue
- send any default string from queue to channel
- kill itself
- apply password-protected username

Tests are continuously run using Travis-CI:
[![Build Status](https://travis-ci.org/synthomat/pealbot.png)](https://travis-ci.org/synthomat/pealbot)

## License
Copyright (c) 2012 Synthomat

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at  

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
