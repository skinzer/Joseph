from setuptools import setup

version = "0.0.1"
setup(
    name="Joseph",
    version=version,
    description="A home automation platform with framework aspirations",
    author="Niek Keijzer",
    author_email="info@niekkeijzer.com",
    license="MIT",
    url="https://github.com/NiekKeijzer/joseph",
    packages=["joseph"],
    install_requires=[
        "janus",
    ],
    tests_require=[
        "asynctest",
    ],
    test_suite="tests"
)
