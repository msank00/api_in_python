format:
	isort -rc -y .
	black -l 79 .

cleanup:
	rm log/*.log


