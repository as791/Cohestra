package io.cohestra.sdk;

/** Wraps non-2xx HTTP responses from the Cohestra API. */
public class CohestraException extends RuntimeException {
    private final int statusCode;
    private final String body;

    public CohestraException(int statusCode, String body) {
        super("Cohestra API error %d: %s".formatted(statusCode, body));
        this.statusCode = statusCode;
        this.body = body;
    }

    public int statusCode() { return statusCode; }
    public String body() { return body; }
}
