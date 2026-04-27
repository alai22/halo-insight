---
title: "(NI) ME21-US66. Show how many pets of the same breed use Halo Collar at the moment"
sidebar_label: "(NI) ME21-US66. Show how many pets of the same breed use Halo Collar at the moment"
sidebar_position: 348
author: "Kiryl Trafimau"
---

| Document status | Document owner | Link to JIRA Issue | Related requirements |
|---|---|---|---|
| APPROVED |
| Kiryl Trafimau |
| HALO-17863 - MOB, BE: Quick win: Same breed users (adding your pet step) Ready for Development |
| ME21-US15. Assign pet(Won't do) ME07-US92. Quick win for Edit Pet Profile |Acceptance criteria Possible message combinations

User story

As an app user, I want to see that other dogs of the same breed use Halo so that I feel more trust to the product.

# Acceptance criteria

| AC# | Description | Comments, designs |
|---|---|---|
| ME21-US66-AC01 | Precondition: I am on the 'Adding Your Pet' screenWHEN I click 'Next'THEN I can see popover: -Icon as per design-Title: 'Did You Know?'-Text: depending on filled details, see AC below-Buttons: --'Great!', by click I redirected to Setting up wi-fi screen --'Back', by click popover is closed, user stays at the 'Adding Your Pet' screenNote: Bold in AC means these words should be in bold on popover. | Zeplin |
| ME21-US66-AC02 | Preconditions:I am on the 'Adding Your Pet' screenI selected BreedI not filled Pet BirthdayIF amount of dogs with the same breed in the DB of Halo dogs is 100 or moreWHEN I click 'Next'THEN I see the text on the popover:'[Breed]...there are currently [Amount] in the Halo Pack!'Amount - amount of dogs with the same breed in the DB of Halo dogs.Exception: IF Breed is 'No Breed Specified' app should behave as if Breed was not selected. | Zeplin |
| ME21-US66-AC03 | Preconditions:I am on the 'Adding Your Pet' screenI selected BreedI not filled Pet BirthdayIF amount of dogs with the same breed in the DB of Halo dogs is less than 100 WHEN I click 'Next'THEN I see the text on the popover:'Your dog is a very rare breed. There are currently [Amount] Halo Dogs in the Pack.' Amount - amount of all dogs in the DB of Halo Pets. |  |
| ME21-US66-AC04 | Preconditions:I am on the 'Adding Your Pet' screenI did not select the BreedI filled Pet BirthdayPet's age is 1 year or more, but less than 11 years.WHEN I click 'Next'THEN I see the text on the popover:'There are currently [Amount] Halo Dogs that are [age in full years] years old.' Amount - amount of dogs of the same age (in full years) in the DB of Halo Pets.Exception: If amount=1, then '1 year old', not '1 years old'. |  |
| ME21-US66-AC05 | Preconditions:I am on the 'Adding Your Pet' screenI did not select the BreedI filled Pet BirthdayPet's age is 11 years or more.WHEN I click 'Next'THEN I see the text on the popover:'There are currently [Amount] Halo Dogs that are over 10 years old.'Amount - amount of dogs whose age is more than 10 years. |  |
| ME21-US66-AC06 | Preconditions:I am on the 'Adding Your Pet' screenI did not select the BreedI filled Pet BirthdayPet's age is less than 1 year.WHEN I click 'Next'THEN I see the text on the popover:'There are currently [Amount] Halo Dogs that are 3 months old or less.' -for dogs with age up to 3 full months (inclusive).'There are currently [Amount] Halo Dogs that are between 4 and 6 months old.' -for dogs with age more than 3 full months up to 6 full months (inclusive).'There are currently [Amount] Halo Dogs that are between 7 and 9 months old.' -for dogs with age more than 6 full months up to 9 full months (inclusive).'There are currently [Amount] Halo Dogs that are between 10 and 12 months old.' -for dogs with age more than 9 full months up to 12 months (not inclusive).Amount - amount of dogs of the same age (in each 3-months section) in the DB of Halo Pets. | Zeplin |
| ME21-US66-AC07 | Preconditions:I am on the 'Adding Your Pet' screenI selected BreedI filled Pet BirthdayIF amount of dogs with the same breed in the DB of Halo dogs is 100 or moreWHEN I click 'Next'THEN I see the text on the popover:The 1st paragraph is a text from ME21-US66-AC02The 2nd paragraph is a text from ME21-US66-AC04 (if dog age is between 1 year and 10 years) OR ME21-US66-AC05 (if dog's age 11+ years) OR ME21-US66-AC06 (if dog's age is less than 1 year). |  |
| ME21-US66-AC08 | Preconditions:I am on the 'Adding Your Pet' screenI selected BreedI filled Pet BirthdayIF amount of dogs with the same breed in the DB of Halo dogs is less than 100WHEN I click 'Next'THEN I see the text on the popover:The 1st paragraph is a text: 'Your dog is a very rare breed.'The 2nd paragraph is a text from ME21-US66-AC04 (if dog age is between 1 year and 10 years) OR ME21-US66-AC05 or ME21-US66-AC06 (if dog's age is less than 1 year). | Zeplin |
| ME21-US66-AC08 | Preconditions:I am on the 'Adding Your Pet' screenI did not select the BreedI did not fill Pet BirthdayWHEN I click 'Next'THEN I see the text on the popover:'There are currently [Amount] Halo Dogs in the Pack.' Amount - amount of all dogs in the DB of Halo Pets. |  |### Possible message combinations

|  | Age | Breed | Message |
|---|---|---|---|
| 1 | we don't know | we don't know | There are currently [Amount] Halo Dogs in the Pack. |
| 2 | we don't know | popular (100 or more dogs) | '[Breed]...there are currently [Amount] in the Halo Pack!' |
| 3 | we don't know | rare (less than 100 dogs) | Your dog is a very rare breed. There are currently [Amount] Halo Dogs in the Pack. |
| 4 | 1 year or more, no more than 10 years (10 included) | we don't know | There are currently [Amount] Halo Dogs that are [age in full years] years old. |
| 5 | More than 10 years (11+) | we don't know | There are currently [Amount] Halo Dogs that are over 10 years old. |
| 6 | Less than 1 year | we don't know | There are currently [Amount] Halo Dogs that are 3 months old or less. OR There are currently [Amount] Halo Dogs that are between 4 and 6 months old. ORThere are currently [Amount] Halo Dogs that are between 7 and 9 months old. OR There are currently [Amount] Halo Dogs that are between 10 and 12 months old. |
| 7 | 1 year or more, no more than 10 years (10 included) | popular (100 or more dogs) | There are currently [Amount] Halo Dogs identified as a [Breed].There are also [Amount] Halo dogs that are [age in full years] years old. |
| 8 | More than 10 years (11+) | popular (100 or more dogs) | [Breed]...there are currently [Amount]in the Halo Pack!There are also [Amount] Halo Dogs that are over 10 years old. |
| 9 | Less than 1 year | popular (100 or more dogs) | [Breed]...there are currently [Amount]in the Halo Pack!+There are also [Amount] Halo Dogs that are 3 months old or less. ORThere are also [Amount] Halo Dogs that are between 4 and 6 months old. ORThere are also [Amount] Halo Dogs that are between 7 and 9 months old. OR There are also [Amount] Halo Dogs that are between 10 and 12 months old. |
| 11 | 1 year or more, no more than 10 years (10 included) | rare (less than 100 dogs) | Your dog is a very rare breed.There are currently [Amount] Halo Dogs that are [age in full years] years old. |
| 12 | More than 10 years (11+) | rare (less than 100 dogs) | Your dog is a very rare breed.There are currently [Amount] Halo Dogs that are over 10 years old. |
| 13 | Less than 1 year | rare (less than 100 dogs) | Your dog is a very rare breed.+There are currently [Amount] Halo Dogs that are 3 months old or less. ORThere are currently [Amount] Halo Dogs that are between 4 and 6 months old. ORThere are currently [Amount] Halo Dogs that are between 7 and 9 months old. OR There are currently [Amount] Halo Dogs that are between 10 and 12 months old. |
