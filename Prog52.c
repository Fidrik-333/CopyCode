#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define MAX_SYMBOLS 100
#define MAX_LINE_LEN 100

typedef struct {
    char label[20];
    int address;
} Symbol;

typedef struct {
    char mnemonic[10];
    char opcode[3];
} OpCode;

Symbol symtab[MAX_SYMBOLS];
int symcount = 0;

OpCode optab[] = {
    {"MOV", "01"},
    {"ADD", "02"},
    {"SUB", "03"},
    {"END", "00"}
};

int optab_size = 4;

char *get_opcode(char *mnemonic)
{
    int i;

    for (i = 0; i < optab_size; i++) {
        if (strcmp(mnemonic, optab[i].mnemonic) == 0)
            return optab[i].opcode;
    }

    return NULL;
}

void insert_symbol(char *label, int address)
{
    int i;

    for (i = 0; i < symcount; i++) {
        if (strcmp(symtab[i].label, label) == 0) {
            printf("Error: Duplicate symbol %s\n", label);
            exit(1);
        }
    }

    strcpy(symtab[symcount].label, label);
    symtab[symcount].address = address;
    symcount++;
}

int search_symbol(char *label)
{
    int i;

    for (i = 0; i < symcount; i++) {
        if (strcmp(symtab[i].label, label) == 0)
            return symtab[i].address;
    }

    return -1;
}

/* PASS 1 */
void pass1(FILE *source)
{
    char line[MAX_LINE_LEN];
    int locctr = 0;

    while (fgets(line, sizeof(line), source)) {

        char label[20] = "";
        char opcode[20] = "";
        char operand[20] = "";

        char *colon = strchr(line, ':');

        if (colon != NULL) {

            sscanf(line, "%[^:]:", label);

            sscanf(colon + 1, "%s %s", opcode, operand);

            insert_symbol(label, locctr);
        }
        else {
            sscanf(line, "%s %s", opcode, operand);
        }

        if (strcmp(opcode, "END") == 0)
            break;

        if (get_opcode(opcode) != NULL)
            locctr++;
        else {
            printf("Error: Invalid opcode %s\n", opcode);
            exit(1);
        }
    }

    rewind(source);
}

/* PASS 2 */
void pass2(FILE *source, FILE *output)
{
    char line[MAX_LINE_LEN];
    int address = 0;

    fprintf(output,
            "LOC\tLABEL\tOPCODE\tOPERAND\tMACHINE_CODE\n");

    while (fgets(line, sizeof(line), source)) {

        char label[20] = "";
        char opcode[20] = "";
        char operand[20] = "";

        char *colon = strchr(line, ':');

        if (colon != NULL) {

            sscanf(line, "%[^:]:", label);

            sscanf(colon + 1, "%s %s", opcode, operand);
        }
        else {
            sscanf(line, "%s %s", opcode, operand);
        }

        if (strcmp(opcode, "END") == 0)
            break;

        char *op = get_opcode(opcode);

        if (op == NULL) {
            printf("Error: Invalid opcode %s\n", opcode);
            exit(1);
        }

        int operand_address = 0;

        if (strlen(operand) > 0) {

            if (strcmp(operand, "A") == 0 ||
                strcmp(operand, "B") == 0 ||
                strcmp(operand, "C") == 0) {

                operand_address = 0;
            }
            else {
                operand_address = search_symbol(operand);

                if (operand_address == -1) {
                    printf("Error: Undefined symbol %s\n", operand);
                    exit(1);
                }
            }
        }

        fprintf(output,
                "%d\t%s\t%s\t%s\t%s%02d\n",
                address,
                label[0] ? label : "-",
                opcode,
                operand[0] ? operand : "-",
                op,
                operand_address);

        address++;
    }
}

int main()
{
    FILE *source;
    FILE *output;

    source = fopen("source.asm", "r");

    if (source == NULL) {
        printf("Error: Cannot open source.asm\n");
        return 1;
    }

    pass1(source);

    output = fopen("output.obj", "w");

    if (output == NULL) {
        printf("Error: Cannot create output.obj\n");
        fclose(source);
        return 1;
    }

    pass2(source, output);

    fclose(source);
    fclose(output);

    printf("Two-pass assembler completed.\n");
    printf("Output saved in output.obj\n");

    return 0;
}
