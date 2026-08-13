#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define MAX_SYMBOLS 100
#define MAX_LINE_LEN 100
#define MAX_OPCODE_LEN 10

typedef struct {
    char label[20];
    int address;
} Symbol;

typedef struct {
    char mnemonic[10];
    char opcode[3];
} OpCode;

/* Symbol table */
Symbol symtab[MAX_SYMBOLS];
int symcount = 0;
int locctr = 0;

/* Opcode table */
OpCode optab[] = {
    {"MOV", "01"},
    {"ADD", "02"},
    {"SUB", "03"},
    {"END", "00"}
};

int optab_size = sizeof(optab) / sizeof(optab[0]);

/* Get machine opcode */
char *get_opcode(char *mnemonic)
{
    int i;

    for (i = 0; i < optab_size; i++) {
        if (strcmp(mnemonic, optab[i].mnemonic) == 0)
            return optab[i].opcode;
    }

    return NULL;
}

/* Insert symbol into symbol table */
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

/* Search symbol table */
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

    while (fgets(line, MAX_LINE_LEN, source)) {

        char label[20] = "";
        char opcode[20] = "";
        char operand[20] = "";

        sscanf(line, "%s %s %s", label, opcode, operand);

        /* Check whether first word is a label */
        if (strchr(label, ':') != NULL) {

            label[strlen(label) - 1] = '\0';

            insert_symbol(label, locctr);

            /* Shift opcode and operand */
            strcpy(opcode, operand);
            operand[0] = '\0';

            /* Get remaining operand */
            char temp[20];

            if (sscanf(line, "%*s %s %s", opcode, temp) == 2)
                strcpy(operand, temp);
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

    while (fgets(line, MAX_LINE_LEN, source)) {

        char label[20] = "";
        char opcode[20] = "";
        char operand[20] = "";

        sscanf(line, "%s %s %s", label, opcode, operand);

        /* If label is present */
        if (strchr(label, ':') != NULL) {

            label[strlen(label) - 1] = '\0';

            strcpy(opcode, operand);

            char temp[20];

            if (sscanf(line, "%*s %s %s", opcode, temp) == 2)
                strcpy(operand, temp);
            else
                operand[0] = '\0';
        }

        if (strcmp(opcode, "END") == 0)
            break;

        char *op = get_opcode(opcode);

        if (op == NULL) {
            printf("Error: Invalid opcode %s\n", opcode);
            exit(1);
        }

        /*
         * For this lab example:
         * A, B and C are treated as registers
         * and encoded as address 00.
         */
        int operand_address = 0;

        if (strlen(operand) > 0) {

            int value = search_symbol(operand);

            if (value != -1) {
                operand_address = value;
            }
            else if (strcmp(operand, "A") == 0 ||
                     strcmp(operand, "B") == 0 ||
                     strcmp(operand, "C") == 0) {
                operand_address = 0;
            }
            else {
                printf("Error: Undefined symbol %s\n", operand);
                exit(1);
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

    /* Pass 1 */
    pass1(source);

    /* Pass 2 */
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
