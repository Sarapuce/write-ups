# Trucha bug
To keep my secrets, I protected my application with my RSA implementation to require a signature when someone tries to access it. Nobody will ever be able to get my precious flag... Right?


## Context
For this challenge, we have a source file and an address where the program is probably running. This challenge will probably include signature verification with RSA.

---

## 🕵️ What do we have in this file ?
Let's first have a look to this source file starting by the main function. The only interresting part in this function is when the option "flag" option is selected :

```
int main(void) {
    // ...
    int input_size = 100;
    char input[input_size];

    fgets(input, input_size, stdin);
    remove_trailing_line_feed(input); # Our input is stored in the input variable with the ending "\n" replaced by \x00

    if (strstr(input, "flag") != NULL) {
        printf("Okay, but before that I need you to prove me I can trust you... Please send me now the raw RSA signature of what you just sent, as a base 10 number.\n");
        fflush(stdout);

        char signature_str[1000];
        fgets(signature_str, 1000, stdin);
        remove_trailing_line_feed(signature_str); # Our string representing our number is stored in signature_str variable

        mpz_t signature;
        mpz_init(signature);                                     # The signature is converted in integer here.
        int failure = mpz_set_str(signature, signature_str, 10); # We use mpz here to manipulate big number
        if (failure) {
            printf("That's not a base 10 number.\n");
            fflush(stdout);
            return 1;
        }

        if (check_signature(input, strlen(input), signature)) { # We call the check_signature function with our 2 inputs
            FILE* f = fopen("flag.txt", "r");                   # The goal is to land here
            int flag_size = 100;
            char flag[flag_size];
            fgets(flag, flag_size, f);

            printf("Sure, here is the flag: %s\n", flag);
            fflush(stdout);
        }
        // ...
}
```

We can see that our first input is compared with the string "flag" with the strstr function.
```
if (strstr(input, "flag") != NULL) {
```

Then, the program asks us a number in base 10 and calls the `check_signature` function with our 2 inputs as arguments.
```
if (check_signature(input, strlen(input), signature)) {
```
Let's inspect the `check_signature` function :

```
bool check_signature(unsigned char* content, int content_len, mpz_t signature) {
    hash_state md;
    sha256_init(&md);

    unsigned char computed_hash[SHA256_SIZE];
    sha256_process(&md, content, content_len); # content is our first input
    sha256_done(&md, computed_hash);

    char computed_hash_str[SHA256_SIZE * 2 + 1]; // don't forget the + 1 for the null byte

    for (int i = 0; i < SHA256_SIZE; i++) {
        sprintf(&computed_hash_str[i * 2], "%02x", computed_hash[i]);
    }
```

In this first part, the sha256 of our input is calculated and stored in `computed_hash_str`. In other world, the sha256 of "flag" is stored into `computed_hash`

I won't analyse the next part of the code in detail mainly because it is big integer manipulation :
```
mpz_t computed_hash_mpz;
    mpz_init(computed_hash_mpz);
    mpz_set_str(computed_hash_mpz, computed_hash_str, 16);

    mpz_t n;
    mpz_init(n);
    mpz_set_str(n, PKEY_N, 10);

    // the + 5 and + 4 in the following piece of code are because mpz_out_raw exports not just the raw bytes of the number, but a specific sequence consisting of :
    // - 4 bytes of size information, containing the size in bytes of the number
    // - the bytes of the number itself
    // - 1 ending null byte
    unsigned char in_mem_buf[SHA256_SIZE + 5];
    unsigned char decrypted_hash[SHA256_SIZE];

    mpz_t dec_sig;
    mpz_init(dec_sig);
    mpz_powm_ui(dec_sig, signature, PKEY_E, n);

    FILE* in_mem_buf_f = fmemopen(in_mem_buf, SHA256_SIZE + 5, "w");
    mpz_out_raw(in_mem_buf_f, dec_sig);
    fclose(in_mem_buf_f);

    memcpy(decrypted_hash, in_mem_buf + 4, SHA256_SIZE);
```

But some lines catch our attention :
<br><br>
```
mpz_powm_ui(dec_sig, signature, PKEY_E, n);
```
We are raising our second input to power E modulus n (This is the RSA signature)
</br><br>

```
return strncmp(computed_hash, decrypted_hash, SHA256_SIZE) == 0;
```
We are supposed to find a number which will be equal to the sha256 of "flag" once computed with RSA if we want this function to return `True`
<br><br>

This is impossible, it should be a bug somewhere to bypass that.

---

## 🌊 Want to install homebrew channel ?

Let's dig a little more about the title of this challenge. When you search "Trucha bug" on Google, you quickly understand that it is a bug used to execute unsigned code on the early day of the Wii. Does it seem familiar ? We also want to bypass a signature check. On this [page](https://wiibrew.org/wiki/Signing_bug) we have an explanation of how this exploit works.

A developper used the `strncmp` function to compare raw hex values. Indeed the `strncmp` function compare two strings until the number of character checked reachs the size passed as argument or **when the first NULL bytes appears**. And if there two NULL bytes at the same place, with the same characters before, the fonction will return 0.

> Example :
> `strncmp("a\x00b", "a\x00a", 3) -> OK`

We are lucky, our developper did the same mistake in the code we saw earlier

```
return strncmp(computed_hash, decrypted_hash, SHA256_SIZE) == 0;
```

Now, our plan is simple, get `computed_hash` and `decrypted_hash` start by the NULL byte. If we succeed to do this, the check will be passed and no other bytes will be compared.

---

## ⚔️ Let's get armed

As we saw before `decrypted_hash` is our signature raised at a certain power. If we use 0, we should get a big array full of zero. One problem solved. 
> :bulb: If for some reason, it was impossible to set the second input as 0, we could have brutforce this value until we get the NULL byte at start of `decrypted_hash`

For `computed_hash` things might be more complicated, how can we change the value of the sha256 if the only input value possible is "flag" ?
Hopefully for us, our developer doesn't seem to like string comparison. To check if we entered "flag", he used the function `strstr` which **searches substring in another string** and not an exact match between strings.

 We can try to to input "flagblablabla" and it still works :
```
What do you want? Please select one of these:
- the date
- the flag
- the answer to life, the universe and everything
flagblablabla
Okay, but before that I need you to prove me I can trust you... Please send me now the raw RSA signature of what you just sent, as a base 10 number.
```

This is great for us, because we can set what we want in input as long as it contains flag. Let's try to find a word that contains "flag" which generates a sha256 starting with the NULL byte.

`sha256.py` will append 2 chars at the end of the word flag and print every result which generate a sha256 starting with the NULL byte

```
$ python3 sha256.py 
flagwR
flagz1
...
```
Let's choose "flagz1"

>If like me you're not sure that everything will work as expected, you can rebuild the binary with
>`gcc main.c -o main -ltomcrypt -lgmp -g`.
>Make sure to have [tomcrypt](https://github.com/libtom/libtomcrypt) and [gmp](https://askubuntu.com/questions/207724/how-to-install-the-latest-gmp-library-in-12-04) installed.
>Now, you're free to use your favorite debuger to see what's inside the memory.
>Or use printf like me...

Let's send our payload to the server :
```
$ python3 main.py
[+] Received : What do you want? Please select one of these:
- the date
- the flag
- the answer to life, the universe and everything
[+] Sent flagz1

[+] Received : Okay, but before that I need you to prove me I can trust you... Please send me now the raw RSA signature of what you just sent, as a base 10 number.
[+] Sent 0

[+] Received : Sure, here is the flag: RM{1n_m3m0ry_0f_b3n_bush1g_by3r}
```

Very good challenge and very nice tribute to Ben “bushing” Byer who worked on several console hacks 🕊