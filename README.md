# garmin-f6p-korean-support
Repo to add Korean language support to a non-APAC Fenix 6 Pro.

## Resources

* [Installing a language pack](https://forums.garmin.com/sports-fitness/healthandwellness/f/vivoactive-3-3-music/137682/how-to-install-a-language-pack?pifragment-1301=2#pifragment-1301=3)
* [Installing Korean to Edge 1040](https://blog.naver.com/samnim33/223061915944)
* [Various links and resources](https://www.reddit.com/r/Garmin/comments/107xrvu/is_there_a_way_to_display_korean_on_garmin_fenix/k3pv5xv/)
* [Installing Korean language pack and font on Edge 530](https://gall.dcinside.com/mgallery/board/view/?id=cycle&no=127841&page=1)
  * [Derivative tutorial for Edge 530](https://www.clien.net/service/board/cm_bike/17204379?od=T31&po=0&category=0&groupCd=)
  * [Another derivative tutorial for Edge 530](https://blog.naver.com/vegandinosaur/222710264767)

## Logic

* Garmin watches have language files in the format of `.ln4` under the `./Primary/Garmin/Text` directory, where each `.ln4` file seems to follow the following format:
  * First line: `{gen_num-model-language_num|version}`
  * Line 2 onwards: `{hexademical_key|translation}`
* The list of languages used in the watch are configured within `GarminDevice.xml`
* To add language support for an officially unsupported language, the watch needs to have a `.ln4` file with the `translation` items, and the `.ln4` file needs to be listed within the `GarminDevice.xml` file.
* The list of `hexademical_key`s is different across generations, but there are many common items that persist across generations. Therefore, if a `.ln4` for the desired language is not available, it should be possible to reverse-engineer the `.ln4` file with the following approach:
  1. Get a `.ln4` file for the language from a different generation watch, if available
  2. Get the list of keys used in the system from an `.ln4` file unused by the user
  3. Map the translations from the different generation `.ln4` file to the keys from step 2, for the overlapping items
  4. For items that are not found in the different generation watch, use auto-translation to translate the items with no direct translations
  5. Overwrite the contents of the unused `.ln4` file (step 2) with the mapped + auto-translated items (step 4)
  6. Set the system language to the language using the modified `.ln4` file

## Conclusion

* For Fenix 6-generation Garmin watches, it's not possible to display CJK (Chinese, Japanese and Korean) letters on a non-APAC model, even with a corresponding `.ln4` file loaded in the watch. This is because even with the correct `.ln4` file, the watch needs to have a different font installed in the system to render and display the items in the `.ln4` file. 
* However, unlike previous watches or bike computers, the font files for Fenix 6-generation watches are not exposed as system files, but embedded deep within the OS that is inaccessible to the end user.
* However, it _may_ be possible to use the `.ln4` substitution method to change the system UI language to a different language, provided the language does not use a different character set (ex: Spanish on a European model), but this is unconfirmed.
* Although it is not possible to add language support for Fenix 6 generation watches, Fenix 7 and onwards generation watches support Unicode out-of-the-box, so this issue becomes irrelevant for the more modern Garmin watches.