CREATE OR REPLACE PROCEDURE summarize_admin_dashboard (
    p_admin_count       OUT NUMBER,
    p_user_count        OUT NUMBER,
    p_group_count       OUT NUMBER,
    p_post_count        OUT NUMBER,
    p_comment_count     OUT NUMBER,
    p_message_count     OUT NUMBER
)
AS
BEGIN
    -- Count of admin users
    SELECT COUNT(*) INTO p_admin_count
    FROM felhasznalok
    WHERE admin = 1;

    -- Total registered users
    SELECT COUNT(*) INTO p_user_count
    FROM felhasznalok;

    -- Total distinct groups
    SELECT COUNT(*) INTO p_group_count
    FROM csoportok;

    -- Total posts
    SELECT COUNT(*) INTO p_post_count
    FROM bejegyzesek;

    -- Total comments
    SELECT COUNT(*) INTO p_comment_count
    FROM kommentek;

    -- Total messages
    SELECT COUNT(*) INTO p_message_count
    FROM uzenetek;
END;
/
