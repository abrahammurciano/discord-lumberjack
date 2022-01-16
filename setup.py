from setuptools import setup
import discord_lumberjack

with open("README.md", "r", encoding="utf-8") as readme_file:
	long_description = readme_file.read()

with open("requirements.txt") as requirements_file:
	requirements = requirements_file.readlines()

setup(
	name="discord-lumberjack",
	version=discord_lumberjack.__version__,
	description="A Python logging handler which sends its logs to a Discord Channel",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/abrahammurciano/discord-lumberjack",
	author=discord_lumberjack.__author__,
	author_email="abrahammurciano@gmail.com",
	license="GPLv3",
	packages=[
		discord_lumberjack.__name__,
		discord_lumberjack.handlers.__name__,
		discord_lumberjack.message_creators.__name__,
	],
	install_requires=requirements,
	package_data={discord_lumberjack.__name__: ["py.typed"]},
	classifiers=[
		"Development Status :: 5 - Production/Stable",
		"Intended Audience :: Developers",
		"License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
		"Operating System :: OS Independent",
		"Programming Language :: Python :: 3",
		"Programming Language :: Python :: 3.8",
		"Programming Language :: Python :: 3.9",
		"Programming Language :: Python :: 3.10",
	],
)
