# Strava Heatmap

This project provides a heatmap visualization of Strava activities by using the
Strava API and ipyleaflet.

1. Follow the instructions on
   [stravalib](https://stravalib.readthedocs.io/en/latest/get-started/authenticate-with-strava.html#step-1-create-an-application-in-your-strava-account)
   to create an application.

2. Set the following environment variables with the values obtained from your
   Strava application:
   - `STRAVA_CLIENT_ID`
   - `STRAVA_CLIENT_SECRET`

3. Run the authentication script to obtain and save your access tokens.

   ```sh
   python -m _strava.authentication
   ```

4. Set the following environment variables with the values obtained from the
   authentication script:
   - `STRAVA_ACCESS_TOKEN`
   - `STRAVA_REFRESH_TOKEN`
   - `STRAVA_EXPIRES_AT`

5. Run Quarto commands as normal.
