# The Sheep Binder — build kit

This folder makes a Sheep Binder app (the demo or a customer's copy) from the newest
Gehret Sheep Co code. It isn't part of the app; the app is the files one folder up.

## Building a customer's copy (for Claude, in a new chat)

1. Read the project doc `claude/sheep-binder-spec.md` and Ian's filled-in `INTAKE-FORM.md`.
2. Get the code:
   ```
   git clone --depth 3 https://github.com/iangehret-netizen/gehretsheepco src
   git clone --depth 3 https://github.com/iangehret-netizen/thesheepbinder tsb
   ```
3. Copy `tsb/kit/intake-template.json` to `<customer>/intake.json` and fill it in from the form.
   - `storagePrefix` and `collection`: a short code unique to this customer (e.g. `smcl:` / `smcl`).
     Every app on iangehret-netizen.github.io shares one web address, so the prefix is what keeps
     each farm's records apart on a phone.
   - `palette`: when the form says "match the logo", pick dark/accent/accentLight/accentMid from it.
   - `logo`: their PNG. `logoOnDark` if their logo is dark and won't show on the black header.
     `icon` for a separate square home-screen icon.
4. Build and check:
   ```
   python3 tsb/kit/build.py --src src --intake <customer>/intake.json --out <customer>/app
   python3 tsb/kit/test/walk.py <customer>/app shots        # every tab at phone size
   python3 tsb/kit/test/remove.py <customer>/app shots      # Remove examples
   ```
   The build stops with "BUILD ERROR" if the Gehret code changed in a way it doesn't expect;
   fix the matching line in `build.py` and rerun.
5. Records to load: turn their files into an app backup (`{"app":..,"created":..,"data":{"sheepwrld:...": "<json>"}}`,
   the same shape Settings → Backup & Restore downloads), and they restore it once in
   Settings → Backup & Restore. Or add the records as a one-time seed.
6. Firebase (their own free project): create Firestore, paste the generated `firestore.rules`, turn on
   Email/Password and Anonymous sign-in, add the sign-in user (its password is the passcode), and add
   `iangehret-netizen.github.io` under Authorized domains.
7. Push the `app` folder to their repo and turn on GitHub Pages (main branch, root).

## Updating every copy when Gehret gets new features

Pull the newest `gehretsheepco`, bump `version` in each intake.json, rebuild and push.
Customers' records aren't touched: they live on their phones and in their own Firebase.

## What the build changes

- Removes all of Gehret's records, names, logo and Firebase project.
- Settings move into `config.js` (name, storage prefix, Firebase, sync email, years).
- Colors swap to the palette; logos and icons are made from the customer's logo, or the Sheep Binder wordmark.
- Adds `examples.js`: 2–3 test entries in every tab on first open, and Settings → Help → **Remove examples**,
  which takes out only those (ids starting `ex-`) and keeps anything the user entered.
