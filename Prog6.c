#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define MAX 20
#define LEN 100

typedef struct {
    char name[LEN];
    int mdt_index;
} MNTEntry;

typedef struct {
    char line[LEN];
} MDTEntry;

MNTEntry MNT[MAX];
MDTEntry MDT[MAX];

int mntc = 0;
int mdtc = 0;

/* Store macro definition in MNT and MDT */
void store_macro(FILE *fp)
{
    char line[LEN];
    char name[LEN];

    /* Read macro name */
    if (fscanf(fp, "%s", name) != 1)
        return;

    strcpy(MNT[mntc].name, name);
    MNT[mntc].mdt_index = mdtc;
    mntc++;

    /* Consume the rest of the macro-name line */
    fgets(line, LEN, fp);

    /* Read parameter definition line */
    if (fgets(line, LEN, fp) != NULL) {
        strcpy(MDT[mdtc].line, line);
        mdtc++;
    }

    /* Read macro body until MEND */
    while (fgets(line, LEN, fp) != NULL) {

        if (strncmp(line, "MEND", 4) == 0)
            break;

        strcpy(MDT[mdtc].line, line);
        mdtc++;
    }

    strcpy(MDT[mdtc].line, "MEND\n");
    mdtc++;
}

/* Find macro in MNT */
int find_macro(char *name)
{
    int i;

    for (i = 0; i < mntc; i++) {
        if (strcmp(MNT[i].name, name) == 0)
            return MNT[i].mdt_index;
    }

    return -1;
}

/* Expand macro */
void expand_macro(int index, char *params)
{
    char original_line[LEN];
    char replaced[LEN];
    char paramsArr[MAX][LEN];

    int p = 0;
    int i;

    /* Split actual parameters */
    char *token = strtok(params, ",");

    while (token != NULL && p < MAX) {

        /* Remove leading spaces */
        while (*token == ' ')
            token++;

        strcpy(paramsArr[p++], token);

        token = strtok(NULL, ",");
    }

    /* Skip parameter definition line */
    index++;

    /* Read macro body */
    while (strcmp(MDT[index].line, "MEND\n") != 0 &&
           strcmp(MDT[index].line, "MEND") != 0) {

        strcpy(original_line, MDT[index].line);

        /*
         * Replace &A, &B, &C...
         * with actual parameters.
         */
        for (i = 0; i < p; i++) {

            char placeholder[10];
            sprintf(placeholder, "&%c", 'A' + i);

            char *pos = strstr(original_line, placeholder);

            while (pos != NULL) {

                char temp[LEN];

                int offset = pos - original_line;

                strcpy(temp, pos + strlen(placeholder));

                original_line[offset] = '\0';

                strcat(original_line, paramsArr[i]);
                strcat(original_line, temp);

                pos = strstr(original_line + offset +
                             strlen(paramsArr[i]),
                             placeholder);
            }
        }

        printf("%s", original_line);

        index++;
    }
}

int main()
{
    FILE *fin;

    char line[LEN];
    char macro_name[LEN];
    char params[LEN];

    fin = fopen("input.asm", "r");

    if (fin == NULL) {
        printf("Cannot open input.asm\n");
        return 1;
    }

    /* Read input file */
    while (fgets(line, LEN, fin) != NULL) {

        /* If MACRO found, store macro definition */
        if (strncmp(line, "MACRO", 5) == 0) {

            store_macro(fin);
        }
        else {

            /* Get first word */
            sscanf(line, "%s", macro_name);

            /* Search macro */
            int idx = find_macro(macro_name);

            if (idx != -1) {

                /* Get parameters */
                char *ptr = strchr(line, ' ');

                if (ptr != NULL) {
                    strcpy(params, ptr + 1);

                    /* Remove newline */
                    params[strcspn(params, "\n")] = '\0';
                }
                else {
                    params[0] = '\0';
                }

                expand_macro(idx, params);
            }
            else {

                /* Normal assembly instruction */
                printf("%s", line);
            }
        }
    }

    fclose(fin);

    return 0;
}
