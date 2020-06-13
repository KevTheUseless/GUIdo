#include <iostream>
#include <string>

void write(); //Accepts text input from user

int main(int argc, char** argv)
{
	if (!argv[1])
	{
		printf("Missing argument.\nUsage: vis <filename>");
		return 0;
	}
	while (true)
	{
		std::string cmd;
		std::cin >> cmd;
		if (cmd == "i")
		{
			freopen(argv[1], "w", stdout);
			write();
		}
		else if (cmd == "a")
		{
			freopen(argv[1], "a", stdout);
			write();
		}
		else if (cmd == "q")
			return 0;
		else
			printf("?\n");
	}
}

void write()
{
	while (true)
	{
		std::string line;
		std::getline(std::cin, line);
		if (line == ".")
		{
			#ifdef _WIN32
				freopen("con", "w", stdout);
			#elif defined __unix__
				freopen("/dev/tty", "w", stdout);
			#endif
			break;
		}
		std::cout << line << std::endl;
	}
}