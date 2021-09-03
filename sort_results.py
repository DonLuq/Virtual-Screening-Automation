# For sorting results if not sorted yet
import sys


def main(*file):
    best_results = {}
    print(file[0][1])
    with open(file[0][1], 'r') as file:
        for line in file.readlines():
            best_results[line.split('->')[0]] = float(line.split('->')[1])

    best_results = sorted(best_results.items(), key=lambda x: x[1], reverse=True)

    with open('best_results.txt', 'w') as file:
        for i in best_results:
            file.write(i[0] + '\t'+str(i[1])+'\n')


if __name__ == '__main__':
    main(sys.argv)
