##
## EPITECH PROJECT, 2022
## B-CNA-410-COT-4-1-trade-marcel.yobo
## File description:
## Makefile
##

SRC = trade.py

NAME = trade

all: $(NAME)

$(NAME): 
	cp -f $(SRC) $(NAME)
	chmod +x $(NAME)

clean:
	rm -f $(NAME)

fclean: clean

re: fclean all