# AM1
`Ajna MultiAgent One` platform to get things done for you from surfing web and taking actions, collecting data, reading and analysing files, planning, coding, research, and
more... to reach the goal given by user.

Let agents do the grunt work for you, while you focus on the big picture.

## Demo Video
Demo video will be released on 11th March 2025 along with UI Release.

## Setup
Execute the following commands to setup the project:
```bash setup.sh```

## Run AM1
Execute the following commands to run the project:
```bash run_dockerized.sh```

## Documentation
Key things to note:
- You can run LLM models locally only if your system has GPU, sufficient RAM, compute and space. Please check the requirements before running the models.
- If you do not have sufficient resources in your local system, you can use LLMs on cloud of your choice. For instance, you will need to specify OpenAI Key in config/local.yml file or as environment variable in your system or dockerfile as applicable. 
- More LLM support will be added soon.
- We have currently integrated MagenticOne (Autogen 0.4.2) for our Multi-Agent Framework. Refer to the documentation of MagenticOne for more details.
- More such frameworks will be added soon so that users can choose which works best for them.
- For privacy, we recommend using any open-source LLM model on your local system with an open source model where data never leaves your system.
- For any queries, you can raise an issue in GitHub repo.
- We will share Contributors guide on 11th March 2025.
- Please note this is an active development product, and we are working on adding more features and support for more frameworks. Things may change rapidly and sometimes break, please do not consider using this for production grade application or critical workflow.
- Feel free to share your feedback and suggestions.
- The project may change rapidly, please keep an eye on the updates and documentation for best use.

## License
This project is licensed under Apache 2.0 License - see the LICENSE file for details.

## References
- [AutoGen](https://github.com/microsoft/autogen)
- [AG2](https://github.com/ag2ai/ag2)
- [OpenAI](https://openai.com)
